echo "Running server.sh"

# Set constants
readonly DATA_MEM_PERCENT = 40
readonly OTHER_SVCS_MEM_PERCENT = 8

#######################################################
############ Turn Off Transparent Hugepages ###########
#######################################################

echo "Turning off transparent hugepages..."

echo "#!/bin/bash
### BEGIN INIT INFO
# Provides:          disable-thp
# Required-Start:    $local_fs
# Required-Stop:
# X-Start-Before:    couchbase-server
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Disable THP
# Description:       disables Transparent Huge Pages (THP) on boot
### END INIT INFO

echo 'never' > /sys/kernel/mm/transparent_hugepage/enabled
echo 'never' > /sys/kernel/mm/transparent_hugepage/defrag
" > /etc/init.d/disable-thp
chmod 755 /etc/init.d/disable-thp
service disable-thp start
update-rc.d disable-thp defaults

#######################################################
################# Set Swappiness to 0 #################
#######################################################

echo "Setting swappiness to 0..."

sysctl vm.swappiness=0
echo "
# Required for Couchbase
vm.swappiness = 0
" >> /etc/sysctl.conf

#######################################################
############### Install Couchbase Server ##############
#######################################################

echo "Installing prerequisites..."
apt-get update
apt-get -y install python-httplib2
apt-get -y install jq

echo "Installing Couchbase Server..."
wget http://packages.couchbase.com/releases/${serverVersion}/couchbase-server-enterprise_${serverVersion}-ubuntu18.04_amd64.deb
dpkg -i couchbase-server-enterprise_${serverVersion}-ubuntu18.04_amd64.deb
apt-get update
apt-get -y install couchbase-server

#######################################################
############## Configure Couchbase Server #############
#######################################################

echo "Configuring Couchbase Server"

echo "Using the settings:"
echo serverVersion ${serverVersion}
echo couchbaseUsername ${couchbaseUsername}
# Use the below line in dev environments if needed
# echo couchbasePassword ${couchbasePassword}
echo services ${services}
echo CLUSTER ${CLUSTER}

NODE_PRIVATE_DNS=`curl -s http://metadata/computeMetadata/v1/instance/hostname`
echo NODE_PRIVATE_DNS: ${NODE_PRIVATE_DNS}

#######################################################
################### Pick Rally Point ##################
#######################################################

# We need to have the data service running on this node to be a potential rally point
if [[ $services =~ "data" ]]
then
  # check if we already have a rally point for the cluster
  rallyPrivateDNS=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
    https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/${CLUSTER}/rallyPrivateDNS \
    | jq ".text" \
    | sed 's/"//g')

  # if not then create and populate it
  if [[ $rallyPrivateDNS == "null" ]]
  then
  curl -s -k -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "X-GFE-SSL: yes" \
    -d "{name: \"projects/${PROJECT_ID}/configs/${CONFIG}/variables/${CLUSTER}/rallyPrivateDNS\", text: \"${NODE_PRIVATE_DNS}\" }" \
    https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables
  fi

  # wait for any parallel writes to happen
  sleep 1

  # read the rally value from the config
  rallyPrivateDNS=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
    https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/${CLUSTER}/rallyPrivateDNS \
    | jq ".text" \
    | sed 's/"//g')
  echo rallyPrivateDNS: ${rallyPrivateDNS}
else
  rallyPrivateDNS=null
  while [[ $rallyPrivateDNS == "null" ]]
  do
    rallyPrivateDNS=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
      https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/${CLUSTER}/rallyPrivateDNS \
      | jq ".text" \
      | sed 's/"//g')
    echo rallyPrivateDNS: ${rallyPrivateDNS}
  done
fi

#######################################################
####### Wait until web interface is available #########
####### Needed for the cli to work	          #########
#######################################################

checksCount=0

printf "Waiting for server startup..."
until curl -o /dev/null -s -f http://localhost:8091/ui/index.html || [[ $checksCount -ge 50 ]]; do
   (( checksCount += 1 ))
   printf "." && sleep 3
done
echo "server is up."

if [[ "$checksCount" -ge 50 ]]
then
  echo "ERROR: Couchbase Webserver is not available after script Couchbase REST readiness retry limit"
fi

#######################################################
############# Configure with Couchbase CLI ############
#######################################################

cd /opt/couchbase/bin/

echo "Running couchbase-cli node-init"
./couchbase-cli node-init \
  --cluster=$NODE_PRIVATE_DNS \
  --node-init-hostname=$NODE_PRIVATE_DNS \
  -u=$couchbaseUsername \
  -p=$couchbasePassword

if [[ $rallyPrivateDNS == $NODE_PRIVATE_DNS ]]
then
  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=$((DATA_MEM_PERCENT * totalRAM / 100000))
  indexRAM=$((8 * totalRAM / 100000))

  echo "Running couchbase-cli cluster-init"
    ./couchbase-cli cluster-init \
    --cluster=$NODE_PRIVATE_DNS \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --index-storage-setting=memopt \
    --cluster-analytics-ramsize=$indexRAM \
    --cluster-fts-ramsize=$indexRAM \
    --cluster-eventing-ramsize=$indexRAM \
    --cluster-username=$couchbaseUsername \
    --cluster-password=$couchbasePassword \
    --services=${services}
else
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "SUCCESS: Server added" && ! $output =~ "Node is already part of cluster." ]]
  do
    output=`./couchbase-cli server-add \
      --cluster=$rallyPrivateDNS \
      -u=$couchbaseUsername \
      -p=$couchbasePassword \
      --server-add=$NODE_PRIVATE_DNS \
      --server-add-username=$couchbaseUsername \
      --server-add-password=$couchbasePassword \
      --services=${services}`
    echo server-add output \'$output\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=`./couchbase-cli rebalance \
      --cluster=$rallyPrivateDNS \
      -u=$couchbaseUsername \
      -p=$couchbasePassword`
    echo rebalance output \'$output\'
    sleep 10
  done

fi

#######################################################
##### Wait until all nodes report healthy status ######
#######################################################

healthyNodes=0
checksCount=0

echo "Waiting for all healthy nodes..."
until [[ $healthyNodes -eq $nodeCount ]] || [[ $checkCount -ge 50 ]]; do
  echo "Healthy nodes check - $healthyNodes/$nodeCount"
  healthyNodes=$(curl -s \
    -u "$couchbaseUsername:$couchbasePassword" \
    http://localhost:8091/pools/nodes \
    | grep -o "\"status\":\"healthy\"" | wc -l)
  (( checksCount += 1 ))
  sleep 3
done
echo "All nodes are healthy - $healthyNodes/$nodeCount."
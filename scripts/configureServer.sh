echo "Running configureServer"

echo "Using the settings:"
echo couchbaseUsername \'$couchbaseUsername\'
echo couchbasePassword \'$couchbasePassword\'
echo services \'$services\'

#######################################################
################### Pick Rally Point ##################
#######################################################

apt-get -y install jq

ACCESS_TOKEN=$(curl -s -H "Metadata-Flavor:Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token | awk -F\" '{ print $4 }')
PROJECT_ID=$(curl -s -H "Metadata-Flavor:Google" http://metadata.google.internal/computeMetadata/v1/project/project-id)
DEPLOYMENT=`hostname | cut -d "-" -f 1`
CLUSTER=`hostname | cut -d "-" -f 2`
CONFIG=${DEPLOYMENT}-${CLUSTER}-runtimeconfig

# 1. Add nodePrivateDNS to runtime config
nodePrivateDNS=`curl -s http://metadata/computeMetadata/v1beta1/instance/hostname`
hostname=`hostname`
curl -s -k -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "X-GFE-SSL: yes" \
  -d "{name: \"projects/${PROJECT_ID}/configs/$CONFIG/variables/nodeList/${hostname}\", text: \"${nodePrivateDNS}\" }" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables

# 2. Get nodeCount from runtime config
VARIABLE_KEY=nodeCount
nodeCount=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/${VARIABLE_KEY} \
  | jq ".text" \
  | sed 's/"//g')

# 3. while ...
# a. Get number of nodes currently in runtime config
VARIABLE_KEY=nodeList/
nodeList=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/${VARIABLE_KEY})
echo nodeList: ${nodeList}

variables=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables?returnValues=True)

lengthOfVariables=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables?returnValues=True \
  | jq ".variables"
  | jq length)
echo lengthOfVariables: ${lengthOfVariables}

# b. If number of nodes currently in runtime config == nodeCount then pick a rally point

#placeholder.  This creates a cluster per node
rallyPrivateDNS=${nodePrivateDNS}

#######################################################
############# Configure with Couchbase CLI ############
#######################################################

cd /opt/couchbase/bin/

echo "Running couchbase-cli node-init"
./couchbase-cli node-init \
  --cluster=$nodePrivateDNS \
  --node-init-hostname=$nodePrivateDNS \
  --user=$couchbaseUsername \
  --pass=$couchbasePassword

if [[ $rallyPrivateDNS == $nodePrivateDNS ]]
then
  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=$((50 * $totalRAM / 100000))
  indexRAM=$((15 * $totalRAM / 100000))

  echo "Running couchbase-cli cluster-init"
  ./couchbase-cli cluster-init \
    --cluster=$nodePrivateDNS \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --cluster-username=$couchbaseUsername \
    --cluster-password=$couchbasePassword \
    --services=${services}
else
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePrivateDNS:8091 added" && ! $output =~ "Node is already part of cluster." ]]
  do
    output=`./couchbase-cli server-add \
      --cluster=$rallyPrivateDNS \
      --user=$couchbaseUsername \
      --pass=$couchbasePassword \
      --server-add=$nodePrivateDNS \
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
      --user=$couchbaseUsername \
      --pass=$couchbasePassword`
    echo rebalance output \'$output\'
    sleep 10
  done

fi

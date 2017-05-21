echo "Running configureServer"

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'

##### Advice from Chris
# Now, add code in your startup script that runs on each VM.
# Have that VM
# 1. register it's name under nodenames/
# 2. read the variables in nodenames
# if you get nodecount items, then sort the 5 items and pick the first one
# else, sleep and try the read again

rallyPrivateDNS=''
nodePrivateDNS=`curl http://metadata/computeMetadata/v1beta1/instance/hostname`

cd /opt/couchbase/bin/

echo "Running couchbase-cli node-init"
./couchbase-cli node-init \
  --cluster=$nodePrivateDNS \
  --node-init-hostname=$nodePrivateDNS \
  --node-init-data-path=/mnt/datadisk/data \
  --node-init-index-path=/mnt/datadisk/index \
  --user=$adminUsername \
  --pass=$adminPassword

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
    --cluster-username=$adminUsername \
    --cluster-password=$adminPassword \
    --services=data,index,query,fts
else
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePrivateDNS:8091 added" && ! $output =~ "Node is already part of cluster." ]]
  do
    vm0PrivateDNS=`host vm0 | awk '{print $1}'`
    output=`./couchbase-cli server-add \
      --cluster=$rallyPrivateDNS \
      --user=$adminUsername \
      --pass=$adminPassword \
      --server-add=$nodePrivateDNS \
      --server-add-username=$adminUsername \
      --server-add-password=$adminPassword \
      --services=data,index,query,fts`
    echo server-add output \'$output\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=`./couchbase-cli rebalance \
      --cluster=$rallyPrivateDNS \
      --user=$adminUsername \
      --pass=$adminPassword`
    echo rebalance output \'$output\'
    sleep 10
  done

fi

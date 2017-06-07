echo "Running configureServer"

echo "Using the settings:"
echo couchbaseUsername \'$couchbaseUsername\'
echo couchbasePassword \'$couchbasePassword\'
echo services \'$services\'

##### This part doesn't work at the moment
gcloud beta runtime-config configs variables get-value nodeCount --config-name ben3-cluster1-runtimeconfig
gcloud beta runtime-config configs variables set nodeList/nodeA nodea --is-text  --config-name [resource config name]
gcloud beta runtime-config configs variables list  --filter=nodeList  --config-name [resource config name]

rallyPrivateDNS=''
nodePrivateDNS=`curl http://metadata/computeMetadata/v1beta1/instance/hostname`

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

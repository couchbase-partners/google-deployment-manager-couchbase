echo "Running configureServer"

echo "Using the settings:"
echo couchbaseUsername \'$couchbaseUsername\'
echo couchbasePassword \'$couchbasePassword\'
echo services \'$services\'

ACCESS_TOKEN=$(curl -s -H "Metadata-Flavor:Google" http://metadata/computeMetadata/v1/instance/service-accounts/default/token | awk -F\" '{ print $4 }')
INSTANCE_NAME=$(curl -s -H "Metadata-Flavor:Google" http://metadata/computeMetadata/v1/instance/name)
RUNTIME_CONFIG_URL=$(curl -s -H "Metadata-Flavor:Google" http://metadata/computeMetadata/v1/instance/attributes/status-config-url)
RUNTIME_CONFIG_PATH=$(echo "$RUNTIME_CONFIG_URL" | sed 's|https\?://[^/]\+/v1\(beta1\)\?/||')
VARIABLE_PATH=$(curl -s -H "Metadata-Flavor:Google" http://metadata/computeMetadata/v1/instance/attributes/status-variable-path)

ACTIONBASE64=$(echo -n "$ACTION" | base64)
PAYLOAD=$(printf '{"name": "%s", "value": "%s"}' "$RUNTIME_CONFIG_PATH/variables/$VARIABLE_PATH/$ACTION/$INSTANCE_NAME" "$ACTIONBASE64")
echo "Posting software startup $ACTION status"
curl -s -X POST -d "$PAYLOAD" -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" "$RUNTIME_CONFIG_URL/variables"

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

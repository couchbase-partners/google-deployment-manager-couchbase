echo "Running configureSyncGateway"

echo "Using the settings:"
echo couchbaseUsername ${couchbaseUsername}
echo couchbasePassword ${couchbasePassword}
echo services ${services}
echo DEPLOYMENT ${DEPLOYMENT}
echo CLUSTER ${CLUSTER}

#######################################################
################### Pick Rally Point ##################
#######################################################

apt-get -y install jq

ACCESS_TOKEN=$(curl -s -H "Metadata-Flavor:Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token | awk -F\" '{ print $4 }')
PROJECT_ID=$(curl -s -H "Metadata-Flavor:Google" http://metadata.google.internal/computeMetadata/v1/project/project-id)
CONFIG=${DEPLOYMENT}-${CLUSTER}-runtimeconfig

nodePrivateDNS=`curl -s http://metadata/computeMetadata/v1beta1/instance/hostname`
echo nodePrivateDNS: ${nodePrivateDNS}

# Get nodeCount from runtimeconfig
nodeCount=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/nodeCount \
  | jq ".text" \
  | sed 's/"//g')
echo nodeCount: ${nodeCount}

liveNodeCount=0
while [[ $liveNodeCount -lt $nodeCount ]]
do
  # Get number of nodes currently in runtime config
  liveNodeCount=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
    https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/?filter=projects%2F${PROJECT_ID}%2Fconfigs%2F${CONFIG}%2Fvariables%2FnodeList \
    | jq ".variables | length")
  echo liveNodeCount: ${liveNodeCount}
  sleep 10
done

serverDNS=$(curl -s -H "Authorization":"Bearer ${ACCESS_TOKEN}" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/?filter=projects%2F${PROJECT_ID}%2Fconfigs%2F${CONFIG}%2Fvariables%2FnodeList\&returnValues=True \
  | jq ".variables | sort_by(.text)" \
  | jq ".[0].text" \
  | sed 's/"//g')
echo serverDNS: ${serverDNS}

echo '
{
  "log": ["*"],
  "databases": {
    "db": {
      "server": "http://${serverDNS}:8091",
      "bucket": "default",
      "users": { "GUEST": { "disabled": false, "admin_channels": ["*"] } }
    }
  }
}
' > /home/sync_gateway/sync_gateway.json

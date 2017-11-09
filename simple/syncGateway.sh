echo "Running syncGateway.sh"

echo "Installing Couchbase Sync Gateway..."
wget https://packages.couchbase.com/releases/couchbase-sync-gateway/${syncGatewayVersion}/couchbase-sync-gateway-enterprise_${syncGatewayVersion}_x86_64.deb
dpkg -i couchbase-sync-gateway-enterprise_${syncGatewayVersion}_x86_64.deb

echo "Configuring Couchbase Sync Gateway..."
file="/home/sync_gateway/sync_gateway.json"
echo '
{
  "interface": "0.0.0.0:4984",
  "adminInterface": "0.0.0.0:4985",
  "log": ["*"]
}
' > ${file}
chmod 755 ${file}
chown sync_gateway ${file}
chgrp sync_gateway ${file}

# Need to restart to load the changes
service sync_gateway stop
service sync_gateway start

#######################################################
####### Wait until web interface is available #########
#######################################################

checksCount=0

printf "Waiting for server startup..."
until curl -o /dev/null -s -f http://localhost:4985/_admin || [[ $checksCount -ge 50 ]]; do
   (( checksCount += 1 ))
   printf "." && sleep 3
done
echo "server is up."
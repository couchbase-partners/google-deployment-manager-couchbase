echo "Running syncGateway.sh"
echo "Installing Couchbase Sync Gateway..."

wget https://packages.couchbase.com/releases/couchbase-sync-gateway/1.4.1/couchbase-sync-gateway-enterprise_1.4.1-3_x86_64.deb
dpkg -i couchbase-sync-gateway-enterprise_1.4.1-3_x86_64.deb

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

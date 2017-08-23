echo "Running installServer"

#######################################################
############ Turn Off Transparent Hugepages ###########
#######################################################

echo "Turning off transparent hugepages..."

# Please look at http://bit.ly/1ZAcLjD as for how to PERMANENTLY alter this setting.

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

# Please look at http://bit.ly/1k2CtNn as for how to PERMANENTLY alter this setting.

sysctl vm.swappiness=0
echo "
# Required for Couchbase
vm.swappiness = 0" >> /etc/sysctl.conf

#######################################################
################## Install Couchbase ##################
#######################################################

echo "Installing Couchbase..."

# Using these instructions
# https://developer.couchbase.com/documentation/server/4.6/install/ubuntu-debian-install.html
wget http://packages.couchbase.com/releases/4.6.2/couchbase-server-enterprise_4.6.2-ubuntu14.04_amd64.deb
dpkg -i couchbase-server-enterprise_4.6.2-ubuntu14.04_amd64.deb
apt-get update
apt-get -y install couchbase-server

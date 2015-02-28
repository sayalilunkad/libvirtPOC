#!/usr/bin/env bash
set -o errexit -o nounset
TOP_DIR=$(cd $(dirname "$0")/.. && pwd)
source "$TOP_DIR/config/paths"
source "$CONFIG_DIR/credentials"
source "$LIB_DIR/functions.guest"
source "$CONFIG_DIR/admin-openstackrc.sh"
exec_logfile

indicate_current_auto

#------------------------------------------------------------------------------
# Set up OpenStack neutron LBaaS for controller node.
# http://docs.openstack.org/admin-guide-cloud/content/install_neutron-lbaas-agent.html
#------------------------------------------------------------------------------

echo "Configuring neutron lbaas for controller node."
conf=/etc/neutron/neutron.conf

# Configure network plugin parameters
iniset_sudo $conf DEFAULT service_plugins "router,lbaas"

echo "Restarting neutron service."
sudo service neutron-server restart

# Configure openstack dashboard
function check_dashboard_settings {
    local memcached_conf=/etc/memcached.conf
    local dashboard_conf=/etc/openstack-dashboard/local_settings.py

    # Enabling Neutron LBaaS on Horizon
    echo "Enabling neutron LBaaS on horizon."
    sudo sed -i "s/'enable_lb': False/\'enable_lb\': True/" $dashboard_conf
}

echo "Checking dashboard configuration."
check_dashboard_settings

echo "Reloading apache and memcached service."
sudo service apache2 restart
sudo service memcached restart

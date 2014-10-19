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
# Create the external network and a subnet on it.
#------------------------------------------------------------------------------

# Work around neutron client failing with unsupported locale settings
if [[ "$(neutron --help)" == "unsupported locale setting" ]]; then
    echo "Locale not supported on node, setting LC_ALL=C."
    export LC_ALL=C
fi

echo "Waiting for neutron to start."
until neutron net-list >/dev/null 2>&1; do
    sleep 1
done

echo "Creating the external network."
neutron net-create ext-net --router:external=True

echo "Creating a subnet on the external network."
neutron subnet-create ext-net \
    --name ext-subnet \
    --allocation-pool start="$FLOATING_IP_START,end=$FLOATING_IP_END" \
    --disable-dhcp \
    --gateway "$EXTERNAL_NETWORK_GATEWAY" \
    "$EXTERNAL_NETWORK_CIDR"

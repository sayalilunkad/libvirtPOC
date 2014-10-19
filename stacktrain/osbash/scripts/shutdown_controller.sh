#!/usr/bin/env bash
set -o errexit -o nounset
TOP_DIR=$(cd $(dirname "$0")/.. && pwd)
source "$TOP_DIR/config/paths"
source "$LIB_DIR/functions.guest"

indicate_current_auto

exec_logfile

echo "Shutting down the controller node."

ssh \
    -o "UserKnownHostsFile /dev/null" \
    -o "StrictHostKeyChecking no" \
    -i "$HOME/.ssh/vagrant" \
    controller-mgmt \
    sudo /sbin/shutdown -P now

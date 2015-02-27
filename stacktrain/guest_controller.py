from os.path import basename
from fabric.api import run
from fabric.api import put
from fabric.api import sudo
from fabric.api import env

env.user = 'osbash'
env.password = 'osbash'
env.hosts = ['192.168.122.43']


def autostart(source):
    put(source, '/home/osbash/autostart/%s' % basename(source))
    run('sudo chmod a=r+w+x /home/osbash/autostart/%s' % basename(source))
    run('sudo bash /home/osbash/autostart/%s' % basename(source))

run('rm -rf /home/osbash/autostart')
run('mkdir autostart')

put('/home/sayali/Repositories/training-guides/labs/config', '/home/osbash')
put('/home/sayali/Repositories/training-guides/labs/lib', '/home/osbash')
put('/home/sayali/Repositories/training-guides/labs/log', '/home/osbash')

autostart('/home/sayali/Repositories/training-guides/labs/autostart/init_controller_node.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/etc_hosts.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/apt_install_mysql.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/install_rabbitmq.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/setup_keystone.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/setup_glance.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/setup_nova_controller.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/setup_neutron_controller.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/setup_cinder_controller.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/setup_horizon.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/config_external_network.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/config_tenant_network.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/setup_lbaas_controller.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/shutdown_controller.sh')

from os.path import basename
from fabric.api import run
from fabric.api import put
from fabric.api import env
import os

# env.user = 'osbash'
# env.password = 'osbash'
# env.hosts = ['192.168.122.43', '10.10.10.51', '10.10.10.52', '10.10.10.53']

ABS_DIR = os.path.abspath('fabfile.py').rsplit('/', 1)[0]


def net():
    env.user = 'osbash'
    env.password = 'osbash'
    env.hosts = ['192.168.122.43']


def net_controller():
    env.user = 'osbash'
    env.password = 'osbash'
    env.hosts = ['10.10.10.51']


def net_compute():
    env.user = 'osbash'
    env.password = 'osbash'
    env.hosts = ['10.10.10.53']


def net_network():
    env.user = 'osbash'
    env.password = 'osbash'
    env.hosts = ['10.10.10.52']


def autostart(source):
    put(source, '/home/osbash/autostart/%s' % basename(source))
    run('sudo chmod a=r+w+x /home/osbash/autostart/%s' % basename(source))
    run('sudo bash /home/osbash/autostart/%s' % basename(source))


def base():
    run('mkdir autostart')
    run('mkdir log')
    put(ABS_DIR + '/osbash/config', '/home/osbash')
    put(ABS_DIR + '/osbash/lib', '/home/osbash')

    autostart(ABS_DIR + '/osbash/scripts/osbash/base_fixups.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/apt_init.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/apt_pre-download.sh')
    autostart(ABS_DIR + '/osbash/scripts/zero_empty.sh')
    autostart(ABS_DIR + '/osbash/scripts/shutdown.sh')


def controller_init():
    run('rm -rf /home/osbash/autostart')
    run('rm -rf /home/osbash/log')
    run('mkdir autostart')
    run('mkdir log')
    run('sudo apt-get update')
    put(ABS_DIR + '/osbash/config', '/home/osbash')
    put(ABS_DIR + '/osbash/lib', '/home/osbash')

    autostart(ABS_DIR + '/osbash/scripts/osbash/init_controller_node.sh')
    autostart(ABS_DIR + '/osbash/scripts/etc_hosts.sh')


def controller():
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/apt_install_mysql.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/install_rabbitmq.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_keystone.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_glance.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_nova_controller.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_neutron_controller.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_cinder_controller.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_horizon.sh')
    autostart(ABS_DIR + '/osbash/scripts/config_external_network.sh')
    autostart(ABS_DIR + '/osbash/scripts/config_tenant_network.sh')
    autostart(ABS_DIR + '/osbash/scripts/setup_lbaas_controller.sh')
    autostart(ABS_DIR + '/osbash/scripts/shutdown_controller.sh')


def compute_init():
    run('rm -rf /home/osbash/autostart')
    run('rm -rf /home/osbash/log')
    run('mkdir autostart')
    run('mkdir log')
    run('sudo apt-get update')
    autostart(ABS_DIR + '/osbash/scripts/osbash/init_compute_node.sh')
    autostart(ABS_DIR + '/osbash/scripts/etc_hosts.sh')


def compute():
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_nova_compute.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_neutron_compute.sh')
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_cinder_volumes.sh')
    autostart(ABS_DIR + '/osbash/scripts/shutdown_controller.sh')


def network_init():
    run('rm -rf /home/osbash/autostart')
    run('rm -rf /home/osbash/log')
    run('mkdir autostart')
    run('mkdir log')
    run('sudo apt-get update')
    autostart(ABS_DIR + '/osbash/scripts/osbash/init_network_node.sh')
    autostart(ABS_DIR + '/osbash/scripts/etc_hosts.sh')


def network():
    autostart(ABS_DIR + '/osbash/scripts/ubuntu/setup_neutron_network.sh')
    autostart(ABS_DIR + '/osbash/scripts/shutdown_controller.sh')

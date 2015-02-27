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

run('mkdir autostart')

put('/home/sayali/Repositories/training-guides/labs/config', '/home/osbash')
put('/home/sayali/Repositories/training-guides/labs/lib', '/home/osbash')
put('/home/sayali/Repositories/training-guides/labs/log', '/home/osbash')

autostart('/home/sayali/Repositories/training-guides/labs/scripts/osbash/base_fixups.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/apt_init.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/ubuntu/apt_pre-download.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/zero_empty.sh')
autostart('/home/sayali/Repositories/training-guides/labs/scripts/shutdown.sh')

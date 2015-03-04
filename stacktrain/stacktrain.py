#!/usr/bin/python2.7

import vm_tasks
import network_tasks
import os
import time


print "Fetching required images"
os.system("python2 get_image.py")

print "Create the networks"
try:
    mgmt_net = network_tasks.Network('mgmt', '10.10.10.1', 'vibr10')
    mgmt_net.create_network()
    mgmt_net.close()
except:
    pass

try:
    data_net = network_tasks.Network('data', '10.20.20.1', 'vibr11')
    data_net.create_network()
    data_net.close()
except:
    pass

try:
    api_net = network_tasks.Network('api', '192.168.100.1', 'vibr12')
    api_net.create_network()
    api_net.close()
except:
    pass


print "Creating temporary disk"
time.sleep(10)
vm = vm_tasks.Domain()

try:
    vm.create_domain('base', 'kernel')

    print 'Installing the base VM: ',
    while vm.vm_status('base'):
        time.sleep(10)
        print '=',
    print '[Done]'
except:
    pass

print "Destroys temporary domain"
vm.destroy_domain('base')
os.system('git checkout xml/.')
time.sleep(10)
print "Creating base disk"
vm.create_domain('template2', 'hd')
time.sleep(30)

os.system("fab net base")
time.sleep(30)
print "Destroys base domain"
vm.destroy_domain('template2')

os.system('git checkout xml/.')
time.sleep(10)
print "Creating controller node"
vm.create_domain('controller', 'hd')
time.sleep(100)
while not vm.vm_status('controller'):
    time.sleep(5)
print "Configuring networks in controller node"
os.system("fab net_init_controller controller_init")
time.sleep(30)
print "Power off controller node"
vm.power_off('controller')
while vm.vm_status('controller'):
    time.sleep(5)
time.sleep(30)
print "Power on controller"
vm.power_on('controller')
while not vm.vm_status('controller'):
    time.sleep(5)
time.sleep(100)
os.system("fab net_controller controller")
time.sleep(30)

print "Power off controller"
vm.power_off('controller')
while vm.vm_status('controller'):
    time.sleep(5)
time.sleep(10)
print "Creating compute node"
vm.create_domain('compute', 'hd')

while not vm.vm_status('compute'):
    time.sleep(30)
time.sleep(30)
print "Configuring network for compute node"
os.system("fab net_init_compute compute_init")
time.sleep(30)

print "Power off compute"
vm.power_off('compute')
while vm.vm_status('compute'):
    time.sleep(5)
time.sleep(30)
print "Power on controller"
vm.power_on('controller')
while not vm.vm_status('controller'):
    time.sleep(30)
time.sleep(60)
print "Power on compute"
vm.power_on('compute')
while not vm.vm_status('compute'):
    time.sleep(30)
time.sleep(100)
os.system("fab net_compute compute")
time.sleep(50)

print "Power off controller"
vm.power_off('controller')
while vm.vm_status('controller'):
    time.sleep(5)
print "Power off compute"
time.sleep(10)
vm.power_off('compute')
while vm.vm_status('compute'):
    time.sleep(5)
time.sleep(20)
print "Creating network node"
vm.create_domain('network', 'hd')
while not vm.vm_status('network'):
    time.sleep(30)

time.sleep(30)
os.system("fab net_init_network network_init")
time.sleep(50)

print "Power off network"
vm.power_off('network')
while vm.vm_status('network'):
    time.sleep(5)
print "Power on controller"
vm.power_on('controller')
while not vm.vm_status('controller'):
    time.sleep(30)
time.sleep(100)
print "Power on compute"
vm.power_on('compute')
while not vm.vm_status('compute'):
    time.sleep(30)
time.sleep(100)
print "Power on network"
vm.power_on('network')
while not vm.vm_status('network'):
    time.sleep(30)
time.sleep(100)
os.system("fab net_network network")
time.sleep(50)


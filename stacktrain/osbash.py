import vm_tasks
import network_tasks
import os
import time
"""
print "Fetching required images"
os.system("python2 get_image.py")

print "Create the networks"
mgmt_net = network_tasks.Network('mgmt', '10.10.10.1', 'vibr10')
mgmt_net.create_network()
mgmt_net.close()
data_net = network_tasks.Network('data', '10.20.20.1', 'vibr11')
data_net.create_network()
data_net.close()
api_net = network_tasks.Network('api', '192.168.100.1', 'vibr12')
api_net.create_network()
api_net.close()

print "Creating base disk"
vm = vm_tasks.Domain()
vm.create_domain('base', 'kernel')
vm.destroy_domain('base')
vm.create_domain('template2', 'hd')
time.sleep(10)
os.system("fab net base")
vm.destroy_domain('template2')

print "Creating controller node"
vm.create_domain('controller', 'hd')
time.sleep(20)
print "Configuring networks in controller node"
os.system("fab net controller_init")
print "Restart controller node"
vm.power_off('controller')
time.sleep(30)
vm.power_on('controller')
time.sleep(30)
os.system("fab net_controller controller")
vm.power_off('controller')
time.sleep(30)
print "Creating compute node"
vm = vm_tasks.Domain()
vm.create_domain('compute', 'hd')
time.sleep(20)
print "Configuring network for compute node"
os.system("fab net compute_init")
print "Restart compute node and start controller node"
vm.power_off('compute')
time.sleep(30)
vm.power_on('controller')
time.sleep(30)
vm.power_on('compute')
time.sleep(30)
os.system("fab net_compute compute")
"""
vm = vm_tasks.Domain()
vm.power_off('controller')
time.sleep(30)
vm.power_off('compute')
time.sleep(30)
print "Creating network node"
vm.create_domain('network', 'hd')
time.sleep(30)
os.system("fab net network_init")
vm.power_off('network')
time.sleep(30)
vm.power_on('controller')
time.sleep(30)
vm.power_on('compute')
time.sleep(30)
vm.power_on('network')
time.sleep(30)
os.system("fab net_network network")

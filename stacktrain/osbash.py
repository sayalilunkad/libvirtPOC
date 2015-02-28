import vm_tasks
import network_tasks
import os


os.system("python2 get_image.py")
print "Create the networks"
mgmt_net = network_tasks.Network('mgmt', '10.10.10.0')
mgmt_net.create_network()
mgmt_net.close()
data_net = network_tasks.Network('data', '20.20.20.0')
data_net.create_network()
data_net.close()
api_net = network_tasks.Network('api', '192.168.100.0')
api_net.create_network()
api_net.close()
vm = vm_tasks.Domain()
vm.create_domain('base', 'kernel')
vm.destroy_domain('base')
vm.create_domain('template2', 'hd')
os.system("fab base")
vm.destroy_domain('template2')
vm.create_domain('controller', 'hd')
os.system("fab controller")
vm.create_domain('compute', 'hd')
os.system("fab compute")
vm.create_domain('network', 'hd')
os.system("fab network")

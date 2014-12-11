import libvirt
import sys
from xml.etree import ElementTree as ET

uri = 'qemu:///system'
conn = libvirt.open(uri)
<<<<<<< HEAD


# Get Libvirt version
# getversion
# getLibVersion

# Get CPU information
# getCPUMap
# getMaxVcpus

# Get free memory
# getFreeMemory
# getMemoryParameters

#

'''

import libvirt
conn=libvirt.open("qemu:///system")

for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    infos = dom.info()
    print 'ID = %d' % id
    print 'Name =  %s' % dom.name()
    print 'State = %d' % infos[0]
    print 'Max Memory = %d' % infos[1]
    print 'Number of virt CPUs = %d' % infos[3]
    print 'CPU Time (in ns) = %d' % infos[2]
    print ' '

'''

=======
>>>>>>> 3b50bc5ab0b86c254422c649505b892595d32d69


# Get Libvirt version
# getversion
# getLibVersion

# Get CPU information
# getCPUMap
# getMaxVcpus

# Get free memory
# getFreeMemory
# getMemoryParameters

#

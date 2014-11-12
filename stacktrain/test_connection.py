import libvirt
import sys
from xml.etree import ElementTree as ET

def run():
    URI = "qemu:///system"
    VM = 'vm1'

    conn = libvirt.open(URI)
    dom0 = conn.lookupByName(VM)

    vm_xml = dom0.XMLDesc(0)

    root = ET.fromstring(vm_xml)
    print root

    print ('\n\n\n\n\n\n')

    if conn == None:
        print 'Failed to open connection to the hypervisor'
        sys.exit(1)

    try:
        dom1 = conn.getAllDomainStats()
    except:
        print 'Failed to find the main domain'
        sys.exit(1)

    print "Domain 0: id %d running %s" % (dom0.ID(), dom0.OSType())
    print dom0.info()

    return True

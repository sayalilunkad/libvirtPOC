# Creates a VM

import libvirt


class Domain(object):
    def __init__(self):
        '''Connects to Libvirt
	'''
	uri = 'qemu:///system'
        self.conn = libvirt.open(uri)

    def power_on(self, domain_name):
	'''Powers on the required VM
	'''
        virDomain_obj = self.conn.lookupByName(domain_name)
        virDomain_obj.create()

    def power_off(self, domain_name):
        '''Powers off the required VM
	'''
	virDomain_obj = self.conn.lookupByName(domain_name)
        virDomain_obj.shutdown()

    def create_domain(self, domain_file):
        '''Creates a VM as per XML description
	'''
	fhandle = open(domain_file)
        xml_description = fhandle.read()
        virDomain_obj = self.conn.defineXML(xml_description)

    def destroy_domain(self, domain_name):
	'''Powers off a VM if on and destroys VM completely
	'''
        active_domains = self.conn.listDomainsID()
        virDomain_obj = self.conn.lookupByName(domain_name)
        if virDomain_obj.ID() in active_domains:
            virDomain_obj.destroy()
        virDomain_obj.undefine()

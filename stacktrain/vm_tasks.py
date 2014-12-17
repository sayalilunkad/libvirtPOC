# Creates a VM

import libvirt


class Domain(object):
    def __init__(self):
        uri = 'qemu:///system'
        self.conn = libvirt.open(uri)

    def power_on(self, domain_name):
        dom0 = self.conn.lookupByName(domain_name)
        dom0.create()

    def power_off(self, domain_name):
        dom0 = self.conn.lookupByName(domain_name)
        dom0.shutdown()

    def create_domain(self, domain_file):
        fhandle = open(domain_file)
        xml_description = fhandle.read()
        virDomain_obj = self.conn.defineXML(xml_description)

    def destroy_domain(self, domain_name):
        active_domains = self.conn.listDomainsID()
        dom0 = self.conn.lookupByName(domain_name)
        if dom0.ID() in active_domains:
            dom0.destroy()
        dom0.undefine()

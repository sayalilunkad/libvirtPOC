#!/usr/bin/python

import libvirt
import vm_description as vm


class Domain(object):

    def __init__(self, uri=None):
        '''
        Connects to Libvirt
        '''
        self._uri = uri
        if self._uri is None:
            self._uri = 'qemu:///system'
            self.conn = libvirt.open(self._uri)

    def power_on(self, domain_name):
        '''
        Powers on the required VM
        '''
        try:
            virDomain_obj = self.conn.lookupByName(domain_name)
            virDomain_obj.create()
        except Exception:
            pass

    def power_off(self, domain_name):
        '''
        Powers off the required VM
        '''
        try:
            virDomain_obj = self.conn.lookupByName(domain_name)
            virDomain_obj.shutdown()
        except Exception:
            pass

    def create_domain(self, vm_name, vm_memory='1024000'):
        '''
        Creates a VM as per XML description
        '''
        try:
            vmd = vm.VirtualMachine(vm_name, vm_memory)
            vmd.build_xml_tree()
            fhandle = open('%s.xml' % vm_name, "r")
            xml_description = fhandle.read()
            self.conn.defineXML(xml_description)
        except Exception:
            pass

    def destroy_domain(self, domain_name):
        '''
        Destroys a VM
        '''
        try:
            active_domains = self.conn.listDomainsID()
            virDomain_obj = self.conn.lookupByName(domain_name)
            if virDomain_obj.ID() in active_domains:
                virDomain_obj.destroy()
            virDomain_obj.undefine()
        except Exception:
            pass

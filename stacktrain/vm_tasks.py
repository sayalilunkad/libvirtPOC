#!/usr/bin/python

import libvirt
import os
import generate_xml
# import network_tasks
import storage_tasks

ABS_DIR = os.path.abspath('vm_tasks.py').rsplit('/', 1)[0]


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

    def create_domain(self, domain_name, boot_type, memory=1024000):

        '''
        Creates a VM as per XML file
        '''
        if boot_type == 'kernel':
            self.createBootVol()
        else :
            self.createOtherVols()

        xml = generate_xml.GenerateXml()
        xml.fill_xml_details(domain_name, boot_type, memory)
        try:
            fhandle = open('%s/xml/%s.xml' % (ABS_DIR, domain_name), "r")
            xml_description = fhandle.read()
            self.conn.defineXML(xml_description)
            self.power_on(domain_name)
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
            os.remove('%s/xml/%s.xml' % (ABS_DIR, domain_name))
        except Exception:
            pass

    def take_domain_snapshot(self, domain_name, snapshot_name):
        '''
        Takes snaphot of current state of VirtualMachine
        '''
        xmlDesc = "<domainsnapshot><name>%s</name></domainsnapshot>" \
            % snapshot_name
        try:
            virDomain_obj = self.conn.lookupByName(domain_name)
            virDomain_obj.snapshotCreateXML(xmlDesc, 0)
        except Exception:
            pass

    def createBootVol(self):

        storage = storage_tasks.Storage('base.qcow2', ABS_DIR + '/osbash/img/',
                                        20)
        storage.createStoragePool()
        storage.createStorageVol()
        storage.close()

    def createOtherVols(self):

        storage = storage_tasks.Storage('base.qcow2', ABS_DIR + '/osbash/img/',
                                        20)
        for vol_name in [ 'controller.qcow2', 'network.qcow2', 'compute.qcow2']:
           storage.cloneStorageVol(disk_name)

#!/usr/bin/python

import libvirt
import os
import uuid as uid
from xml.etree import ElementTree as ET


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

    def create_domain_xml(self, domain_name, memory):
        '''
        Creates XML for domain
        '''
        ABS_DIR = os.path.abspath('vm_tasks.py').rsplit('/', 1)[0]
        capabilities = self.conn.getCapabilities()
        ctree = ET.ElementTree(ET.fromstring(capabilities))
        croot = ctree.getroot()
        for host in croot.findall('host'):
            cpu = host.find('cpu')
            self.host_model = cpu.find('model').text
        for guest in croot.findall('guest'):
            arch = guest.find('arch')
            if arch.get('name') == self.conn.getInfo()[0]:
                self.os_type = guest.find('os_type').text
                self.guest_emulator = arch.find('emulator').text
                self.machine_type = arch.find('machine').get('canonical')
        fhandle = open("%s/xml/template.xml" % ABS_DIR, 'rw')
        xml = fhandle.read()
        tree = ET.ElementTree(ET.fromstring(xml))
        root = tree.getroot()
        for name in root.findall('name'):
            name.text = domain_name
        for uuid in root.findall('uuid'):
            uuid.text = str(uid.uuid4())
        for mem in root.findall('memory'):
            mem.text = str(memory)
        for curr_mem in root.findall('currentMemory'):
            curr_mem.text = str(memory)
        for host_os in root.findall('os'):
            host_os.find('type').set('arch', self.conn.getInfo()[0])
            host_os.find('type').set('machine', self.machine_type)
            host_os.find('type').text = self.os_type
            host_os.find('kernel').text = '%s/osbash/img/pxeboot/vmlinuz' % ABS_DIR
            host_os.find('initrd').text = '%s/osbash/img/pxeboot/initrd.gz' % ABS_DIR
        for host_cpu in root.findall('cpu'):
            host_cpu.find('model').text = self.host_model
        for devices in root.findall('devices'):
            devices.find('emulator').text = self.guest_emulator
#        for devices in root.findall('devices'):
#            disk = devices.find('disk')
#            disk.find('source').set('file', '%s/osbash/img/ubuntu-14.04.1-server-amd64.iso' % ABS_DIR)

        tree.write('%s/xml/%s.xml' % (ABS_DIR, domain_name))

    def create_domain(self, domain_name, memory=1024000):
        '''
        Creates a VM as per XML file
        '''
        try:
            self.create_domain_xml(domain_name, memory)
        except RuntimeError as e:
            print "Runtime error({0}):{1}".format(e.errno, e.strerror)
        try:
            fhandle = open('xml/%s.xml' % domain_name, "r")
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
            os.remove('xml/%s.xml' % domain_name)
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

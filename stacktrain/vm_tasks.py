#!/usr/bin/python

import libvirt
import os
import uuid as uid
from xml.etree import ElementTree as ET

import network_tasks as network
import storage_tasks as storage

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

    def create_domain_xml(self, domain_name, memory):
        '''
        Creates XML for domain
        '''
        capabilities = self.conn.getCapabilities()
        croot = ET.fromstring(capabilities)
        host_arch = croot.findtext('./host/cpu/arch')
        host_model = croot.findtext('./host/cpu/model')
        for guest in croot.findall('guest'):
            guest_arch = guest.find('arch').attrib['name']
            if guest_arch == host_arch:
                os_type = guest.findtext('os_type')
                guest_emulator = guest.findtext('./arch/emulator')
                machine_type = guest.find('./arch/machine').attrib['canonical']
        fhandle = open("%s/xml/init.xml" % ABS_DIR, 'rw')
        xmld = fhandle.read()
        tree = ET.ElementTree(ET.fromstring(xmld))
        root = tree.getroot()
        root.find('./name').text = domain_name
        root.find('./uuid').text = str(uid.uuid4())
        root.find('./memory').text = str(memory)
        root.find('./currentMemory').text = str(memory)
        root.find('./os/type').attrib['arch'] = guest_arch
        root.find('./os/type').attrib['machine'] = machine_type
        root.find('./os/type').text = os_type
        root.find('./os/kernel').text = '%s/osbash/img/pxeboot/linux' % ABS_DIR
        root.find('./os/initrd').text = '%s/osbash/img/pxeboot/initrd.gz' % ABS_DIR
        root.find('./cpu/model').text = host_model
        root.find('./devices/emulator').text = guest_emulator
        for d in root.findall('./devices/disk'):
            if d.attrib['device'] == 'cdrom':
                d.find('./source').attrib['file'] = '%s/osbash/img/ubuntu-14.04.1-server-amd64.iso' % ABS_DIR
            elif d.attrib['device'] == 'disk':
                d.find('./source').attrib['file'] = '%s/osbash/img/test.qcow2' % ABS_DIR
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

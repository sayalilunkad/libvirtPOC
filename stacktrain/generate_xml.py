#!/usr/bin/python

import libvirt
import os
import uuid as uid
from xml.etree import ElementTree as ET

ABS_DIR = os.path.abspath('generate_xml.py').rsplit('/', 1)[0]


class GenerateXml(object):

    def __init__(self, uri=None):
        '''
        Connects to Libvirt
        '''
        self._uri = uri
        if self._uri is None:
            self._uri = 'qemu:///system'
            self.conn = libvirt.open(self._uri)

    def get_facts(self):
        '''
        Gets the machine specifications
        '''
        capabilities = self.conn.getCapabilities()
        root = ET.fromstring(capabilities)
        self.host_arch = root.findtext('./host/cpu/arch')
        self.host_model = root.findtext('./host/cpu/model')
        for guest in root.findall('guest'):
            self.guest_arch = guest.find('arch').attrib['name']
            if self.guest_arch == self.host_arch:
                self.os_type = guest.findtext('os_type')
                self.guest_emulator = guest.findtext('./arch/emulator')
                self.machine_type = \
                    guest.find('./arch/machine').attrib['canonical']

    def fill_xml_details(self, domain_name, boot_type, memory):
        '''
        Fills XML details for domain
        '''
        self.get_facts()
        if boot_type == 'kernel':
            template = "%s/xml/template1.xml" % ABS_DIR
        else:
            template = "%s/xml/template2.xml" % ABS_DIR

        fhandle = open(template, 'rw')
        xmld = fhandle.read()
        tree = ET.ElementTree(ET.fromstring(xmld))
        root = tree.getroot()
        root.find('./name').text = domain_name
        root.find('./uuid').text = str(uid.uuid4())
        root.find('./memory').text = str(memory)
        root.find('./currentMemory').text = str(memory)
        root.find('./os/type').attrib['arch'] = self.guest_arch
        root.find('./os/type').attrib['machine'] = self.machine_type
        root.find('./os/type').text = self.os_type
        root.find('./cpu/model').text = self.host_model
        root.find('./devices/emulator').text = self.guest_emulator
        for d in root.findall('./devices/disk'):
            if d.attrib['device'] == 'cdrom':
                d.find('./source').attrib['file'] = \
                    '%s/osbash/img/ubuntu-14.04.1-server-amd64.iso' % ABS_DIR
            elif d.attrib['device'] == 'disk':
                d.find('./source').attrib['file'] = \
                    '%s/osbash/img/test.qcow2' % ABS_DIR
        if boot_type == 'kernel':
            root.find('./os/kernel').text = \
                '%s/osbash/img/pxeboot/linux' % ABS_DIR
            root.find('./os/initrd').text = \
                '%s/osbash/img/pxeboot/initrd.gz' % ABS_DIR
        tree.write('%s/xml/%s.xml' % (ABS_DIR, domain_name))

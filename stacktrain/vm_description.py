import libvirt
import os
import random
import uuid as uid
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement


class VirtualMachine(object):

    def __init__(self, name, mem):
        uri = 'qemu:///system'
        self.conn = libvirt.open(uri)
        self.vm_name = name
        self.vm_memory = mem
        capabilities = self.conn.getCapabilities()
        tree = ET.ElementTree(ET.fromstring(capabilities))
        root = tree.getroot()
        for host in root.findall('host'):
            cpu = host.find('cpu')
            self.host_model = cpu.find('model').text
        for guest in root.findall('guest'):
            arch = guest.find('arch')
            if arch.get('name') == self.conn.getInfo()[0]:
                self.os_type = guest.find('os_type').text
                self.guest_emulator = arch.find('emulator').text
                self.machine_type = arch.find('machine').get('canonical')

    def build_xml_tree(self):
        top = Element('domain')
        top.attrib['id'] = str(random.randint(1, 10))
        top.attrib['type'] = 'kvm'
        name = SubElement(top, 'name')
        name.text = self.vm_name
        uuid = SubElement(top, 'uuid')
        uuid.text = str(uid.uuid4())
        vcpu = SubElement(top, 'vcpu')
        vcpu.text = '1'
        operating_system = SubElement(top, 'os')
        type = SubElement(operating_system, 'type')
        type.attrib['arch'] = self.conn.getInfo()[0]
        type.text = self.os_type
        type.attrib['machine'] = self.machine_type
        boot = SubElement(operating_system, 'boot')
        boot.attrib['dev'] = 'hd'
        cpu = SubElement(top, 'cpu')
        cpu.attrib['match'] = 'exact'
        cpu.attrib['mode'] = 'custom'
        model = SubElement(cpu, 'model')
        model.text = self.host_model
        model.attrib['fallback'] = 'allow'
        memory = SubElement(top, 'memory')
        memory.attrib['unit'] = 'kiB'
        memory.text = self.vm_memory
        on_poweroff = SubElement(top, 'poweroff')
        on_poweroff.text = 'destroy'
        on_reboot = SubElement(top, 'on_reboot')
        on_reboot.text = 'restart'
        on_crash = SubElement(top, 'on_crash')
        on_crash.text = 'restart'
        on_lockfailure = SubElement(top, 'on_lockfailure')
        on_lockfailure.text = 'poweroff'
        pm = SubElement(top, 'pm')
        S3 = SubElement(pm, 'suspend-to-disk')
        S3.attrib['enabled'] = 'no'
        S4 = SubElement(pm, 'suspend-to-mem')
        S4.attrib['enabled'] = 'yes'
        features = SubElement(top, 'features')
        SubElement(features, 'pae')
        SubElement(features, 'acpi')
        SubElement(features, 'apic')
        clock = SubElement(top, 'clock')
        clock.attrib['offset'] = 'localtime'
        timer1 = SubElement(clock, 'timer')
        timer1.attrib['name'] = 'rtc'
        timer1.attrib['tickpolicy'] = 'catchup'
        timer2 = SubElement(clock, 'timer')
        timer2.attrib['name'] = 'pit'
        timer2.attrib['tickpolicy'] = 'delay'
        timer3 = SubElement(clock, 'timer')
        timer3.attrib['name'] = 'hpet'
        timer3.attrib['present'] = 'no'
        devices = SubElement(top, 'devices')
        emulator = SubElement(devices, 'emulator')
        emulator.text = self.guest_emulator
        disk1 = SubElement(devices, 'disk')
        disk1.attrib['type'] = 'file'
        disk1.attrib['device'] = 'cdrom'
        current_dir = os.getcwd()
        source = SubElement(disk1, 'source')
        source.attrib['file'] = '%s/osbash/img/ubuntu-14.04.1-server-amd64.iso' % current_dir
        target = SubElement(disk1, 'target')
        target.attrib['dev'] = 'hdc'
        SubElement(disk1, 'readonly')
        fhandle = open('%s.xml' % self.vm_name, 'w')
        fhandle.write(ET.tostring(top))

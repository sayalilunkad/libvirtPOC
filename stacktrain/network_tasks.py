#!/usr/bin/python

import libvirt
import uuid


class Network:

    def __init__(self,name, network_ip, bridge):

        uri = 'qemu:///system'
        self.conn = libvirt.open(uri)
        self.xmlDesc = '''
<network>
    <name>'''+name+'''</name>
    <uuid></uuid>
    <forward mode='nat'>
        <nat>
            <port start='1024' end='65535'/>
        </nat>
    </forward>
    <ip address="'''+network_ip+'''" netmask="255.255.255.0"/>
    <bridge name="'''+bridge+'''" stp="on" delay="0" />
    <mac address='00:16:3E:5D:C7:EF'/>
</network>
        '''

    def create_network(self):

        try:
            network_domain = self.conn.networkDefineXML(self.xmlDesc)
            network_domain.setAutostart(1)
            network_domain.create()
            print 'Created NAT Network'
            return True

        except Exception:
            return False

    def destroy_network(self):

        try:
            net = self.conn.networkLookupByName('stacktrain_test_net')
            net.destroy()
            return True

        except Exception:
            return False

    def list_networks(self):

        return self.conn.listNetworks()

    def close(self):
        self.conn.close()

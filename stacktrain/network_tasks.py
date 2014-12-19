#!/usr/bin/python

import libvirt
import uuid


class Network:

    def __init__(self):

        uri = 'qemu:///system'
        self.conn = libvirt.open(uri)
        self.xmlDesc = '''
<network ipv6='yes'>
    <name>stacktrain_test_net</name>
    <uuid>7a3b7497-1ec7-8aef-6d5c-38dff9109e93</uuid>
    <bridge name="virbr10" stp="on" delay="0" />
    <mac address='00:16:3E:5D:C7:9E'/>
</network>
        '''

    def create_network(self):

        try:
            self.conn.networkCreateXML(self.xmlDesc)
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

        return self.conn.listAllNetworks()

    def close(self):
        self.conn.close()

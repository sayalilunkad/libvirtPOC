'''
License: Apache2
'''
import sys

import libvirt


class TestConnection():
    '''Testing libvirt connection!'''

    def connect(self):
        '''Open connection to the given libvirt domain.'''

        uri = "qemu:///system"
        return libvirt.open(uri)

    def test_conn(self):
        '''Test the connection.'''

        conn = self.connect()
        if conn is None:
            print('Failed to open connection to the hypervisor')
            return False
        else:
            print('Connection successful')
            conn.close()
            return True

    def get_info(self):
        '''Get some basic information about the libvirt domain.'''

        conn = self.connect()
        print dir(conn)
        try:
            dom_info = conn.getInfo()
            dom_sys_info = conn.getSysinfo()
            print(dom_info)
            print(dom_sys_info)
            conn.close()
            return True

        except Exception:
            print('Failed to find the main domain')
            return False

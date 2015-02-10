#!/usr/bin/python

import subprocess
import os

class Storage:

    def __init__(self, path, name):

        self.canonicalpath = path + '/' + name

    def create_disk(self):

        createdisk = 'fallocate -l 8192M '+ self.canonicalpath
        log = subprocess.Popen(createdisk.split(), stdout=subprocess.PIPE)
        log.communicate()[0]
        return True

    def destroy_disk(self):

        os.remove(self.canonicalpath)
        return True

    def list_disk(self):

        return self.canonicalpath

    def close(self):
        self.conn.close()

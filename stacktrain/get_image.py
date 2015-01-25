#!/usr/bin/python

import os
import urllib

DISTRO = 'ubuntu'
CURRENT_DIR = os.getcwd()
if DISTRO == 'ubuntu':
    urllib.urlretrieve("http://releases.ubuntu.com/14.04/ubuntu-14.04.1-server-amd64.iso", "%s/osbash/img/ubuntu-14.04.1-server-amd64.iso" % CURRENT_DIR)

#!/usr/bin/python
# Checks and retrieves required ISO image for distro.

import os
import sys
import urllib

DISTRO = 'ubuntu'
ABS_DIR = os.path.abspath(sys.argv[0]).rsplit('/', 1)[0]
if DISTRO == 'ubuntu':
    if os.path.exists("%s/osbash/img/ubuntu-14.04.1-server-amd64.iso"
                      % ABS_DIR) is True:
        print 'ISO present.'
    else:
        print 'Downloading ISO.'
        urllib.urlretrieve("http://releases.ubuntu.com/14.04/ubuntu-14.04.1- \
        server-amd64.iso", "%s/osbash/img/ubuntu-14.04.1-server-amd64.iso"
                           % ABS_DIR)

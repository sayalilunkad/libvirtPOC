#!/usr/bin/python
# Checks and retrieves required ISO image for distro.

import os
import sys
import urllib

DISTRO = 'ubuntu'
ABS_DIR = os.path.abspath(sys.argv[0]).rsplit('/', 1)[0]
os.makedirs(ABS_DIR+'/osbash/img/pxeboot/')
if DISTRO == 'ubuntu':
    if os.path.exists("%s/osbash/img/ubuntu-14.04.1-server-amd64.iso"
                      % ABS_DIR) is True:
        print 'ISO present.'
    else:
        print 'Downloading ISO.'
        urllib.urlretrieve("http://releases.ubuntu.com/14.04/ubuntu-14.04.1-server-amd64.iso", "%s/osbash/img/ubuntu-14.04.1-server-amd64.iso" % ABS_DIR)
    print "PXE"
    directory = "%s/osbash/img/pxeboot" % ABS_DIR
    if not os.path.exists(directory):
        os.mkdir(directory)
    if os.path.exists("%s/osbash/img/pxeboot/linux" % ABS_DIR) is True:
        print 'Kernel image present.'
    else:
        print 'Downloading kernel image.'
        urllib.urlretrieve("http://us.archive.ubuntu.com/ubuntu/dists/trusty/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/linux", \
                           "%s/osbash/img/pxeboot/linux" % ABS_DIR)
    if os.path.exists("%s/osbash/img/pxeboot/initrd.gz" % ABS_DIR) is True:
        print 'initrd present.'
    else:
        print 'Downloading initrd'
        urllib.urlretrieve("http://us.archive.ubuntu.com/ubuntu/dists/trusty/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/initrd.gz", \
                           "%s/osbash/img/pxeboot/initrd.gz" % ABS_DIR)


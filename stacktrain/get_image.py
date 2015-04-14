#!/usr/bin/python
# Checks and retrieves required ISO image for distro.

import os
import sys
import urllib

DISTRO = 'centos'
ABS_DIR = os.path.abspath(sys.argv[0]).rsplit('/', 1)[0]

directory = ABS_DIR+'/osbash/img/CentOS/'
if os.path.exists(directory):
    pass
else:
    os.makedirs(directory)

if DISTRO == 'centos':
    if os.path.exists("%s/osbash/img/CentOS/boot.iso"
                      % ABS_DIR) is True:
        print 'ISO present.'
    else:
        print 'Downloading ISO.'
        urllib.urlretrieve("http://mirror.softaculous.com/centos/7/os/x86_64/images/boot.iso", "%s/osbash/img/CentOS/boot.iso" % ABS_DIR)
    print "PXE"
    directory = "%s/osbash/img/CentOS/" % ABS_DIR
    if not os.path.exists(directory):
        os.mkdir(directory)
    if os.path.exists("%s/osbash/img/CentOS/vmlinuz" % ABS_DIR) is True:
        print 'Kernel image present.'
    else:
        print 'Downloading kernel image.'
        urllib.urlretrieve("http://mirror.softaculous.com/centos/7/os/x86_64/images/pxeboot/vmlinuz", \
                           "%s/osbash/img/CentOS/vmlinuz" % ABS_DIR)
    if os.path.exists("%s/osbash/img/CentOS/initrd.img" % ABS_DIR) is True:
        print 'initrd present.'
    else:
        print 'Downloading initrd'
        urllib.urlretrieve("http://mirror.softaculous.com/centos/7/os/x86_64/images/pxeboot/initrd.img", \
                           "%s/osbash/img/CentOS/initrd.img" % ABS_DIR)


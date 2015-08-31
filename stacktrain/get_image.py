#!/usr/bin/python
# Checks and retrieves required ISO image for distro.

import os
import sys
import urllib

DISTRO = 'opensuse'
ABS_DIR = os.path.abspath(sys.argv[0]).rsplit('/', 1)[0]

directory = ABS_DIR+'/osbash/img/OpenSUSE/'
if os.path.exists(directory):
    pass
else:
    os.makedirs(directory)

if DISTRO == 'opensuse':
    print "PXE"
    directory = "%s/osbash/img/OpenSUSE/" % ABS_DIR

    if not os.path.exists(directory):
        os.mkdir(directory)
    if os.path.exists("%s/osbash/img/OpenSUSE/linux" % ABS_DIR) is True:
        print 'Kernel image present.'
    else:
        print 'Downloading kernel image.'
        urllib.urlretrieve("http://download.opensuse.org/distribution/13.2/repo/oss/boot/x86_64/loader/linux", \
                           "%s/osbash/img/OpenSUSE/linux" % ABS_DIR)
    if os.path.exists("%s/osbash/img/OpenSUSE/initrd" % ABS_DIR) is True:
        print 'initrd present.'
    else:
        print 'Downloading initrd'
        urllib.urlretrieve("http://download.opensuse.org/distribution/13.2/repo/oss/boot/x86_64/loader/initrd", \
                           "%s/osbash/img/OpenSUSE/initrd" % ABS_DIR)


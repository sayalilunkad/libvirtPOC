#!/usr/bin/python

import xml.etree.ElementTree as ET
import libvirt


class Storage:

    def __init__(self, diskName, storagePoolPath, diskSize=8,
                 storagePoolName='stacktrain'):

        self.diskName = diskName
        self.diskSize = diskSize
        self.storagePoolPath = storagePoolPath
        self.disktemplate = './xml/storage/disk-template.xml'
        self.pooltemplate = './xml/storage/pool-template.xml'
        self.storageDiskPath = self.storagePoolPath + '/' + self.diskName
        self.conn = libvirt.connect('qemu:///system')
        self._getStorageXML()

    def createStoragePool(self):

        createflag = 0
        createflag |= libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA
        storagePoolXML = self._getStoragePoolXML()
        self.conn.storagePoolDefineXML(storagePoolXML, createflag)
        self.close()
        return True

    def _getStoragePoolXML(self):

        storageTree = ET.parse(self.pooltemplate)
        storageRoot = storageTree.getroot()
        storageRoot.find('./name').text = self.storagePoolName
        storageRoot.find('./path').text = self.storagePoolPath
        return storageTree

    def createStorageVol(self):

        createflag = 0
        createflag |= libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA

        if self.storagePoolName not in self.conn.listAllStoragePools():
            self.createStoragePool()

        storageDiskXML = self._getStorageDiskXML()
        self.conn.pool.createXML(storageDiskXML, createflag)
        self.close()
        return True

    def _getStorageDiskXML(self):

        storageTree = ET.parse(self.disktemplate)
        storageRoot = storageTree.getroot()
        storageRoot.find('./name').text = self.diskName
        storageRoot.find('./capacity').text = self.diskSize
        storageRoot.find('./path').text = self.storageDiskPath
        return storageTree

    def destroyStorageDisk(self):

        self.close()
        return True

    def destroyStoragePool(self):

        self.close()
        return True

    def list_disk(self):

        self.close()
        return

    def close(self):
        self.conn.close()

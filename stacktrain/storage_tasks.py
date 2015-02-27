#!/usr/bin/python

import xml.etree.ElementTree as ET
import libvirt
import os


class Storage:

    def __init__(self, diskName, storagePoolPath, diskSize=8,
                 storagePoolName="stacktrain"):

        self.diskName = diskName
        self.diskSize = diskSize
        self.storagePoolPath = storagePoolPath
        self.storagePoolName = storagePoolName
        self.disktemplate = os.getcwd() + '/xml/storage/' + 'disk-template.xml'
        self.pooltemplate = os.getcwd() + '/xml/storage/' + 'pool-template.xml'
        self.storageDiskPath = self.storagePoolPath + '/' + self.diskName
        self.conn = libvirt.open('qemu:///system')

    def createStoragePool(self):

        self._createStoragePoolXML()
        fhandle = open(self.pooltemplate, 'r')
        poolXML = fhandle.read()

        try:
            pool = self.conn.storagePoolDefineXML(poolXML)
            pool.setAutostart(1)
            pool.create()
        except:
            print "Pool already exists"

        return True

    def _createStoragePoolXML(self):

        storageTree = ET.parse(self.pooltemplate)
        storageRoot = storageTree.getroot()
        storageRoot.find('./name').text = self.storagePoolName

        for target in storageRoot.findall('target'):
            target.find('./path').text = self.storagePoolPath

        storageTree.write(self.pooltemplate)

        return True

    def createStorageVol(self):

        try :
            pool = self.conn.storagePoolLookupByName(self.storagePoolName)
        except Exception:
            self.createStoragePool()
            pool = self.conn.storagePoolLookupByName(self.storagePoolName)

        self._createStorageDiskXML()
        metadataFlag = 0
        metadataFlag |= libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA
        fhandle = open(self.disktemplate, 'r')
        storageXML = fhandle.read()
        pool.createXML(storageXML, metadataFlag)

        return True

    def _createStorageDiskXML(self):

        storageTree = ET.parse(self.disktemplate)
        storageRoot = storageTree.getroot()
        storageRoot.find('./name').text = self.diskName
        storageRoot.find('./capacity').text = str(self.diskSize)

        for target in storageRoot.findall('target'):
            target.find('./path').text = self.storageDiskPath

        storageTree.write(self.disktemplate)

        return storageTree

    def cloneStorageVol(self, newVolumeName):

        createflag = 0
        createflag |= libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA
        base_disk = self.diskName
        self.diskName = newVolumeName
        self._createStorageDiskXML()
        fhandle = open(self.disktemplate, 'r')
        cloneDiskXML = fhandle.read()
        pool = self.conn.storagePoolLookupByName(self.storagePoolName)
        pool.createXMLFrom(cloneDiskXML,
                           pool.storageVolLookupByName(base_disk), createflag)
        self.diskName = base_disk

        return True

    def destroyStoragePool(self):

        pool = self.conn.storagePoolLookupByName(self.storagePoolName)
        try:
            pool.destroy()
            pool.delete()
        except Exception:
            print("Storage Pool does not exist")

        try:
            pool.undefine()
        except:
            print("Storage Pool cannot be undefined")

        return True

    def list_disk(self):

        try:
            pool = self.conn.storagePoolLookupByName(self.storagePoolName)
            diskNames = pool.listAllVolumes()

            for diskname in diskNames:
                diskname = diskname.name()

            return diskNames

        except Exception:
            print('storage pool does not exist')
            return False

    def close(self):
        self.conn.close()

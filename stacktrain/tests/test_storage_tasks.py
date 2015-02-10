from nose.tools import *
import stacktrain.storage_tasks as storage_tasks
import os


path = os.getcwd()
storage = storage_tasks.Storage(path, 'test.qcow2')

def test_create_disk():

    assert storage.create_disk()

def test_list_disk():

    assert (len(storage.list_disk()) > 0)

def test_destroy_disk():

    assert storage.destroy_disk()

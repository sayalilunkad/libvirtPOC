from nose.tools import *
import stacktrain.vm_tasks as vm


def test_create_domain():
    conn = vm.Domain()
    conn.create_domain(domain_name='test_vm')


def test_power_on_vm():
    conn = vm.Domain()
    conn.power_on('test_vm')


def test_power_off_vm():
    conn = vm.Domain()
    conn.power_off('test_vm')


def test_create_snapshot():
    conn = vm.Domain()
    conn.take_domain_snapshot('test_vm', 'test_snap')


def test_destroy_domain():
    conn = vm.Domain()
    conn.destroy_domain('test_vm')

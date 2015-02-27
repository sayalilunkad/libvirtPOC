from nose.tools import *
import stacktrain.vm_tasks as vm


def test_create_domain():
    conn = vm.Domain()
    assert conn.create_domain(domain_name='test_vm', boot_type='hd')


def test_power_on_vm():
    conn = vm.Domain()
    assert conn.power_on('test_vm')


def test_power_off_vm():
    conn = vm.Domain()
    assert conn.power_off('test_vm')


def test_create_snapshot():
    conn = vm.Domain()
    assert conn.take_domain_snapshot('test_vm', 'test_snap')


def test_destroy_domain():
    conn = vm.Domain()
    assert conn.destroy_domain('test_vm')

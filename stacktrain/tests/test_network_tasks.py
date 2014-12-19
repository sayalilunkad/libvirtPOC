from nose.tools import *
import stacktrain.network_tasks as network_tasks


def test_create_network():

    conn = network_tasks.Network()
    status = conn.create_network()
    conn.destroy_network()
    conn.close()
    assert status


def test_destroy_network():

    conn = network_tasks.Network()
    conn.create_network()
    status = conn.destroy_network()
    conn.close()
    assert status


def test_list_networks():

    conn = network_tasks.Network()
    networks = conn.list_networks()
    conn.close()
    assert type(networks) is list

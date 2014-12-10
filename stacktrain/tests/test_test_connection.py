from nose.tools import *
import stacktrain.test_connection as test_connection


def test_conn():

    conn = test_connection.TestConnection()
    assert conn.test_conn()


def test_get_info():

    conn_info = test_connection.TestConnection()
    assert conn_info.get_info()

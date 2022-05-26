import pytest

from itoolkit import iToolKit
from itoolkit.db2.idb2call import iDB2Call

pytestmark = \
    pytest.mark.filterwarnings("ignore:.*iDB2Call.*:DeprecationWarning")

XMLIN = "<?xml version='1.0'?>\n<xmlservice></xmlservice>"

# iuid=None, ipwd=None, idb2='*LOCAL', ictl='*here *cdata',
#                  ipc='*na', isiz=None, ilib=None):


def test_idb2call_transport_minimal_callproc(database_callproc):
    transport = iDB2Call(database_callproc)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    cursor = database_callproc.cursor()

    cursor.callproc.assert_called_once()
    cursor.fetchall.assert_called_once()


def test_idb2call_transport_minimal_execute(database_execute):
    transport = iDB2Call(database_execute)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    cursor = database_execute.cursor()

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()


def test_idb2call_with_ibm_db(mocker, database_callproc):

    ibm_db = mocker.patch('itoolkit.db2.idb2call.ibm_db', create=True)
    Connection = mocker.patch('itoolkit.db2.idb2call.Connection', create=True) # noqa N806

    class MockConn(object):
        pass

    ibm_db.IBM_DBConnection = MockConn
    Connection.return_value = database_callproc

    conn = MockConn()
    transport = iDB2Call(conn)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    Connection.assert_called_once_with(conn)

    cursor = database_callproc.cursor()

    cursor.callproc.assert_called_once()
    cursor.fetchall.assert_called_once()


def test_idb2call_with_uid_pwd(mocker, database_callproc):

    ibm_db = mocker.patch('itoolkit.db2.idb2call.ibm_db', create=True)
    connect = mocker.patch('itoolkit.db2.idb2call.connect', create=True)

    class MockConn(object):
        pass

    ibm_db.IBM_DBConnection = MockConn
    connect.return_value = database_callproc

    user = 'myuser'
    password = 'mypassword'

    transport = iDB2Call(user, password)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    kwargs = dict(database='*LOCAL', user=user, password=password)
    connect.assert_called_once_with(**kwargs)

    cursor = database_callproc.cursor()

    cursor.callproc.assert_called_once()
    cursor.fetchall.assert_called_once()

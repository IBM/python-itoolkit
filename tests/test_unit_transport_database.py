import pytest

from itoolkit import iToolKit, TransportClosedException
from itoolkit.transport import DatabaseTransport

def test_database_transport_callproc(database_callproc):
    transport = DatabaseTransport(database_callproc)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    cursor = database_callproc.cursor()

    cursor.callproc.assert_called_once()
    cursor.__iter__.assert_called_once()


def test_database_transport_execute(database_execute):
    transport = DatabaseTransport(database_execute)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    cursor = database_execute.cursor()

    cursor.execute.assert_called_once()
    cursor.__iter__.assert_called_once()


def test_database_transport_execute_schema(database_execute):
    schema = 'MYSCHEMA'
    transport = DatabaseTransport(database_execute, schema=schema)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    cursor = database_execute.cursor()

    cursor.execute.assert_called_once()
    cursor.__iter__.assert_called_once()

    assert len(cursor.execute.call_args[0]) > 0
    assert schema in cursor.execute.call_args[0][0]


def test_database_transport_callproc_schema(database_execute):
    schema = 'MYSCHEMA'
    transport = DatabaseTransport(database_execute, schema=schema)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    cursor = database_execute.cursor()

    cursor.execute.assert_called_once()
    cursor.__iter__.assert_called_once()

    assert len(cursor.execute.call_args[0]) > 0
    assert schema in cursor.execute.call_args[0][0]


def test_database_transport_call_raises_when_closed(database_execute):
    schema = 'MYSCHEMA'
    transport = DatabaseTransport(database_execute, schema=schema)
    transport.close()

    with pytest.raises(TransportClosedException):
        tk = iToolKit()
        out = transport.call(tk)

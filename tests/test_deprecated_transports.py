import pytest


def test_rest_import_ok():
    from itoolkit.rest.irestcall import iRestCall

    with pytest.deprecated_call():
        iRestCall('https://example.com', 'user', 'password')


def test_db2_import_ok(database):
    from itoolkit.db2.idb2call import iDB2Call

    with pytest.deprecated_call():
        iDB2Call(database)


def test_lib_import_ok():
    from itoolkit.lib.ilibcall import iLibCall

    with pytest.deprecated_call():
        iLibCall()

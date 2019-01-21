import pytest


def test_rest_import_ok():
    with pytest.warns(DeprecationWarning):
        from itoolkit.rest.irestcall import iRestCall # noqa F401


def test_db2_import_ok():
    with pytest.warns(DeprecationWarning):
        from itoolkit.db2.idb2call import iDB2Call # noqa F401


def test_lib_import_ok():
    with pytest.warns(DeprecationWarning):
        from itoolkit.lib.ilibcall import iLibCall # noqa F401

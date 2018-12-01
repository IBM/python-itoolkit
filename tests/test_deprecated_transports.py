import pytest

def test_rest():
    with pytest.warns(DeprecationWarning):
        from itoolkit.rest.irestcall import iRestCall
    
def test_db2():
    with pytest.warns(DeprecationWarning):
        from itoolkit.db2.idb2call import iDB2Call
    
def test_lib():
    with pytest.warns(DeprecationWarning):
        from itoolkit.lib.ilibcall import iLibCall

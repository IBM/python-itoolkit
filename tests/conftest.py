# -*- coding: utf-8 -*-

import pytest

from mock import Mock, MagicMock


class MockTransport(object):
    def __init__(self, out=None):
        self._out = out

    def set_out(self, out):
        self._out = out

    def call(self, tk):
        return self._out


class MockCursor(object):
    def __init__(self):
        pass

    def callproc(self, proc, args):
        return False


class MockDatabase(object):
    def __init__(self):
        pass

    def cursor(self):
        return MockCursor()


@pytest.fixture
def transport():
    return MockTransport()


XML = "<?xml version='1.0'?>\n<xmlservice></xmlservice>"


def mock_database(use_callproc):
    conn = Mock()

    cursor = MagicMock()
    cursor.fetchall.return_value = [(XML,)]

    if use_callproc:
        cursor.callproc.return_value = True
        del cursor.execute
    else:
        cursor.execute.return_value = True
        del cursor.callproc

    conn.cursor.return_value = cursor
    return conn


@pytest.fixture
def database_callproc():
    return mock_database(use_callproc=True)


@pytest.fixture
def database_execute():
    return mock_database(use_callproc=False)


@pytest.fixture
def database_close_exception():
    conn = mock_database(use_callproc=True)
    conn.close.side_effect = RuntimeError
    return conn


@pytest.fixture
def database():
    return mock_database(use_callproc=True)

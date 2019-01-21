# -*- coding: utf-8 -*-

import pytest


class MockTransport(object):
    def __init__(self, out=None):
        self._out = out

    def set_out(self, out):
        self._out = out

    def call(self, tk):
        return self._out


@pytest.fixture
def transport():
    return MockTransport()

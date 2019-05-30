# -*- coding: utf-8 -*-
import sys
from .base import XmlServiceTransport
try:
    from . import _direct
    # Guard against the dummy version of _direct (for non-PASE builds)
    _available = hasattr(_direct, '_xmlservice')
except ImportError:
    _available = False

__all__ = [
    'DirectTransport'
]


class DirectTransport(XmlServiceTransport):
    """Call XMLSERVICE directly in-process using _ILECALL

    Args:
      **kwargs: Base transport options. See `XmlServiceTransport`.
    """
    def __init__(self, **kwargs):
        super(DirectTransport, self).__init__(**kwargs)

    def call(self, tk):
        if not _available:
            raise RuntimeError("Not supported on this platform")

        data = _direct._xmlservice(tk.xml_in(), self.ctl, self.ipc)

        if sys.version_info >= (3, 0):
            return data.decode('utf-8')
        else:
            return data

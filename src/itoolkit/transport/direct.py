# -*- coding: utf-8 -*-
"""
XMLSERVICE direct call (current job)

License:
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.transport import DirectTransport
  itransport = DirectTransport()

Note:
  XMLSERVICE library search order:
  1) environment variable 'XMLSERVICE' (export XMLSERVICE=QXMLSERV)
  2) QXMLSERV -- IBM PTF library (DG1 PTFs)
  3) XMLSERVICE -- download library (crtxml)
"""
import sys
try:
    from . import _direct
    _available = hasattr(_direct, '_xmlservice')
except ImportError:
    # For Sphinx build
    _available = False

__all__ = [
    'DirectTransport'
]


class DirectTransport(object):
    """
    Transport XMLSERVICE direct job call (within job/process calls).

    Args:
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob']
      ipc    (str): optional - XMLSERVICE route for *sbmjob '/tmp/myunique'
      iccsid (int): optional - XMLSERVICE EBCDIC CCSID
      pccsid (int): optional - XMLSERVICE ASCII CCSID

    Returns:
      none
    """

    def __init__(self, ictl=None, ipc=None, iccsid=0, pccsid=1208):
        self.ctl = ictl or '*here *cdata'
        self.ipc = ipc or '*na'

        if iccsid != 0:
            raise ValueError("iccsid must be 0 (job ccsid)")

        if pccsid != 1208:
            raise ValueError("pccsid must be 1208 (UTF-8)")

    def trace_data(self):
        """Return trace driver data.

        Args:
          none

        Returns:
          initialization data
        """
        return "ctl ({}) ipc ({})".format(self.ctl, self.ipc)

    def call(self, itool):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        if not _available:
            raise RuntimeError("Not supported on this platform")

        data = _direct._xmlservice(itool.xml_in(), self.ctl, self.ipc)

        if sys.version_info >= (3, 0):
            return data.decode('utf-8')
        else:
            return data

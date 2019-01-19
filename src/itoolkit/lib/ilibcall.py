# -*- coding: utf-8 -*-
"""
XMLSERVICE direct call (current job)

License:
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.lib.ilibcall import *
  itransport = iLibCall()

Note:
  XMLSERVICE library search order:
  1) environment variable 'XMLSERVICE' (export XMLSERVICE=QXMLSERV)
  2) QXMLSERV -- IBM PTF library (DG1 PTFs)
  3) XMLSERVICE -- download library (crtxml)
"""
import warnings
from ..transport.direct import DirectTransport

warnings.simplefilter('always', DeprecationWarning)
warnings.warn(
    "This module is deprecated, use itoolkit.transport.DirectTransport instead",
    category=DeprecationWarning,
    stacklevel=2)
warnings.simplefilter('default', DeprecationWarning)


class iLibCall(DirectTransport): # noqa N801 gotta live with history
    """
    Transport XMLSERVICE direct job call (within job/process calls).

    Args:
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob']
      ipc    (str): optional - XMLSERVICE job route for *sbmjob '/tmp/myunique'
      iccsid (int): optional - XMLSERVICE EBCDIC CCSID (0 = default jobccsid)
      pccsid (int): optional - XMLSERVICE ASCII CCSID

    Returns:
      none
    """
    pass

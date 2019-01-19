# -*- coding: utf-8 -*-
"""
XMLSERVICE http/rest/web call (Apache job)

License:
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.rest.irestcall import *
  itransport = iRestCall(url,user,password)
"""
import warnings
from ..transport.http import HttpTransport

warnings.simplefilter('always', DeprecationWarning)
warnings.warn(
    "This module is deprecated, use itoolkit.transport.HttpTransport instead",
    category=DeprecationWarning,
    stacklevel=2)
warnings.simplefilter('default', DeprecationWarning)


class iRestCall(HttpTransport): # noqa N801
    """
    Transport XMLSERVICE calls over standard HTTP rest.

    Args:
      iurl   (str): XMLSERVICE url, eg. https://example.com/cgi-bin/xmlcgi.pgm
      iuid   (str): Database user profile name
      ipwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass)
      idb2   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob']
      ipc    (str): optional - XMLSERVICE route for *sbmjob '/tmp/myunique'
      isiz   (str): optional - XMLSERVICE expected max XML output size

    Example:
      from itoolkit.rest.irestcall import *
      itransport = iRestCall(url,user,password)

    Returns:
      none
    """
    pass

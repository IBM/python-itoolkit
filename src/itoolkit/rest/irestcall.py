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
warnings.warn("This module is deprecated, use itoolkit.transport.HttpTransport instead",
                category=DeprecationWarning,
                stacklevel=2)
warnings.simplefilter('default', DeprecationWarning)

class iRestCall(HttpTransport):
    """
    Transport XMLSERVICE calls over standard HTTP rest.

    Args:
      iurl   (str): XMLSERVICE url (https://common1.frankeni.com:47700/cgi-bin/xmlcgi.pgm).
      iuid   (str): Database user profile name
      ipwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass) 
      idb2   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      isiz   (str): optional - XMLSERVICE expected max XML output size, required for DB2 

    Example:
      from itoolkit.rest.irestcall import *
      itransport = iRestCall(url,user,password)

    Returns:
      none
    """
    pass
    

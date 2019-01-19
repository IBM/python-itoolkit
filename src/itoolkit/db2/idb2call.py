# -*- coding: utf-8 -*-
"""
XMLSERVICE db2 call (QSQSRVR job)

License:
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.db2.idb2call import *
  itransport = iDB2Call(user,password)
  -- or --
  conn = ibm_db.connect(database, user, password)
  itransport = iDB2Call(conn)

Note:
  XMLSERVICE library search order:
  1) lib parm -- iDB2Call(...,'XMLSERVICE')
  2) environment variable 'XMLSERVICE' (export XMLSERVICE=XMLSERVICE)
  3) QXMLSERV -- IBM PTF library (DG1 PTFs)

"""
import warnings
from ..transport.database import DatabaseTransport

warnings.simplefilter('always', DeprecationWarning)
warnings.warn(
    "This module is deprecated,"
    " use itoolkit.transport.DatabaseTransport instead",
    category=DeprecationWarning,
    stacklevel=2)
warnings.simplefilter('default', DeprecationWarning)


class iDB2Call(DatabaseTransport): # noqa N801
    """
    Transport XMLSERVICE calls over DB2 connection.

    Args:
      iuid   (str): Database user profile name or database connection
      ipwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass)
      idb2   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob']
      ipc    (str): optional - XMLSERVICE route for *sbmjob '/tmp/myunique'
      isiz   (int): optional - XMLSERVICE expected max XML output size
      ilib   (str): optional - XMLSERVICE library compiled (default QXMLSERV)

    Example:
      from itoolkit.db2.idb2call import *
      itransport = iDB2Call(user,password)
      -- or --
      conn = ibm_db.connect(database, user, password)
      itransport = iDB2Call(conn)

    Returns:
       (obj)
    """
    pass

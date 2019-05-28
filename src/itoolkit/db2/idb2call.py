# -*- coding: utf-8 -*-
import warnings
import os
try:
    import ibm_db
    from ibm_db_dbi import connect, Connection
except ImportError:
    pass
from ..transport.database import DatabaseTransport


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
    def __init__(self, iuid=None, ipwd=None, idb2='*LOCAL', ictl='*here *cdata',
                 ipc='*na', isiz=None, ilib=None):
        warnings.warn(
            "iDB2Call is deprecated, "
            "use itoolkit.transport.DatabaseTransport instead",
            category=DeprecationWarning,
            stacklevel=2)

        if hasattr(iuid, 'cursor'):
            # iuid is a PEP-249 connection object, just store it
            conn = iuid
        elif isinstance(iuid, ibm_db.IBM_DBConnection):
            # iuid is a ibm_db connection object, wrap it in an
            # ibm_db_dbi connection object
            conn = Connection(iuid)
        else:
            # user id and password passed, connect using ibm_db_dbi
            ipwd = ipwd if ipwd else os.getenv('PASSWORD', None)
            conn = connect(database=idb2, user=iuid, password=ipwd)

        if ilib is None:
            ilib = os.getenv('XMLSERVICE', 'QXMLSERV')

        if isiz is not None:
            msg = "isiz is deprecated and ignored"
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)

        super(iDB2Call, self).__init__(conn=conn, ctl=ictl, ipc=ipc,
                                       schema=ilib)

    def call(self, itool):
        """Call XMLSERVICE with accumulated actions.

        Args:
          itool: An iToolkit object

        Returns:
          The XML returned from XMLSERVICE
        """
        return super(iDB2Call, self).call(itool)

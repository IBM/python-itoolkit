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
import os

try:
    import ibm_db
    import ibm_db_dbi
except ImportError:
    pass

class iDB2Call(object):
    """
    Transport XMLSERVICE calls over DB2 connection.

    Args:
      iuid   (str): Database user profile name or database connection
      ipwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass) 
      idb2   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      isiz   (int): optional - XMLSERVICE expected max XML output size, required for DB2 
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
    def __init__(self, iuid=None, ipwd=None, idb2='*LOCAL', ictl='*here *cdata', ipc='*na', isiz=512000, ilib=None):
        if hasattr(iuid, 'cursor'):
            # iuid is a PEP-249 connection object, just store it
            self.conn = iuid
        elif isinstance(iuid, ibm_db.IBM_DBConnection):
            # iuid is a ibm_db connection object, wrap it in a ibm_db_dbi connection object
            self.conn = ibm_db_dbi.Connection(iuid)
        else:
            # user id and password passed, connect using ibm_db_dbi
            ipwd = ipwd if ipwd else os.getenv('PASSWORD', None)
            self.conn = ibm_db_dbi.connect(database=idb2, user=iuid, password=ipwd)
        
        self.ctl = ictl
        self.ipc = ipc
        self.siz = isiz
        self.lib = ilib if ilib else os.getenv('XMLSERVICE', 'QXMLSERV')
        
    def trace_data(self):
        """Return trace driver data.

        Args:
          none

        Returns:
          initialization data
        """
        data = ""
        data += " ctl (" + str(self.ctl) + ")"
        data += " ipc (" + str(self.ipc) + ")"
        data += " siz (" + str(self.siz) + ") (unused)"
        data += " lib (" + str(self.lib) + ")"
        return data
    
    def call(self, itool):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        cursor = self.conn.cursor()
        
        parms = (self.ipc, self.ctl, itool.xml_in())

        if hasattr(cursor, 'callproc'):
            cursor.callproc(self.lib + ".iPLUGR512K", parms)
        else:
            cursor.execute("call {}.iPLUGR512K(?,?,?)".format(self.lib), parms)
        
        xml_out = ""
        for row in cursor:
            xml_out += row[0]
        
        return xml_out.rstrip('\0')
    

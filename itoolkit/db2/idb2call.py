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
import sys
import os
import re
import urllib
if sys.version_info >= (3,0):
  """
  urllib has been split up in Python 3. 
  The urllib.urlencode() function is now urllib.parse.urlencode(), 
  and the urllib.urlopen() function is now urllib.request.urlopen().
  """
  import urllib.request
  import urllib.parse
import xml.dom.minidom
# import inspect
try:
    import ibm_db
except ImportError:
    pass

class iDB2Call:
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
    def __init__(self, iuid, ipwd=0, idb2=0, ictl=0, ipc=0, isiz=0, ilib=0):
        # manditory
        self.uid = iuid
        if not isinstance(self.uid, str):
          if ipwd == 0:
            ipwd = "*NONE"  
        # optional
        if ipwd == 0:
          self.pwd = os.environ['PASSWORD']
        else:
          self.pwd = ipwd
        if idb2 == 0:
          self.db2 = '*LOCAL'
        else:
          self.db2 = idb2
        if ictl == 0:
          self.ctl = '*here *cdata'
        else:
          self.ctl = ictl
        if ipc == 0:
          self.ipc = '*na'
        else:
          self.ipc = ipc
        if isiz == 0:
          self.siz = 512000
        else:
          self.siz = isiz
        if ilib == 0:
          self.lib = os.getenv('XMLSERVICE','QXMLSERV');
        else:
          self.lib = ilib

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
        data += " uid (" + str(self.uid) + ")"
        data += " db2 (" + str(self.db2) + ")"
        data += " siz (" + str(self.siz) + ")"
        data += " lib (" + str(self.lib) + ")"
        return data

    def call(self, itool):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        if isinstance(self.uid, str):
          conn = ibm_db.connect(self.db2, self.uid, self.pwd)
        else:
          conn = self.uid  
        # sql = "call " + self.lib + ".iPLUG512K(?,?,?,?)"
        sql = "call " + self.lib + ".iPLUGR512K(?,?,?)"
        stmt = ibm_db.prepare(conn, sql)
        ipc = self.ipc
        ctl = self.ctl
        xml_in = itool.xml_in()
        xml_out = ""
        ibm_db.bind_param(stmt, 1, ipc, ibm_db.SQL_PARAM_INPUT)
        ibm_db.bind_param(stmt, 2, ctl, ibm_db.SQL_PARAM_INPUT)
        ibm_db.bind_param(stmt, 3, xml_in, ibm_db.SQL_PARAM_INPUT)
        # ibm_db.bind_param(stmt, 4, xml_out, ibm_db.SQL_PARAM_OUTPUT)
        result = ibm_db.execute(stmt) 
        if ( result ):
          row = ibm_db.fetch_tuple(stmt)
          while ( row ):
            for i in row:
              xml_out += i
            row = ibm_db.fetch_tuple(stmt)
        ibm_db.close(conn)
        return xml_out



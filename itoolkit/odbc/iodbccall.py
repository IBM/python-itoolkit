# -*- coding: utf-8 -*-
"""
XMLSERVICE odbc call

License: 
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.odbc.iodbccall import *
  itransport = iODBCCall(user,password)
  -- or --
  conn = ibm_db.connect(database, user, password)
  itransport = iODBCCall(conn)

Note:
  XMLSERVICE library search order:
  1) lib parm -- iODBCCall(...,'XMLSERVICE')
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
import pyodbc

class iODBCCall(object):
    """
    Transport XMLSERVICE calls over ODBC connection.

    Args:
      idsn   (str): 'DRIVER={IBM i Access ODBC Driver};SYSTEM=system.mydomain.com;UID=MYUSER;PASSWORD=PASSWORD'
                    -- or --
                    active odbc connection
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      ilib   (str): optional - XMLSERVICE library compiled (default QXMLSERV)

    Example:
      from itoolkit.odbc.iodbccall import *
      itransport = iODBCCall(user,password)
      -- or --
      conn = ibm_db.connect(database, user, password)
      itransport = iODBCCall(conn)

    Returns:
       (obj)
    """
    def __init__(self, idsn=0, ictl=0, ipc=0, ilib=0):
        # manditory
        self.dsn = idsn
        if ictl == 0:
          self.ctl = '*here *cdata'
        else:
          self.ctl = ictl
        if ipc == 0:
          self.ipc = '*na'
        else:
          self.ipc = ipc
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
        data += " dsn (" + str(self.dsn) + ")"
        data += " ctl (" + str(self.ctl) + ")"
        data += " ipc (" + str(self.ipc) + ")"
        data += " lib (" + str(self.lib) + ")"
        return data

    def call(self, itool):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        if isinstance(self.dsn, str):
          conn = pyodbc.connect(self.dsn)
        else:
          conn = self.dsn
        # create cursor  
        csr = conn.cursor()  
        # call xmlservice
        csr.execute("call " + self.lib + ".iPLUGR512K(?,?,?)", ipc, clt, itool.xml_in())
        # fetch all rows (xml document)
        xml_out = ""
        rows = csr.fetchall()
        for row in rows:
          xml_out += row
        # close
        csr.close()
        del csr
        conn.close()
        # return xml
        return xml_out



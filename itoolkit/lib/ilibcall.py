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
    import itoolkit.itoollib
except ImportError:
    pass

class iLibCall(object):
    """
    Transport XMLSERVICE direct job call (within job/process calls).

    Args:
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      iccsid (int): optional - XMLSERVICE EBCDIC CCSID [0,37,...] 0 = default jobccsid (1.2+)
      pccsid (int): optional - XMLSERVICE ASCII CCSID [0,1208, ...] 0 = default 1208 (1.2+)

    Returns:
      none
    """
    def __init__(self, ictl=0, ipc=0, iccsid=0, pccsid=0):
        if ictl == 0:
          self.ctl = '*here *cdata'
        else:
          self.ctl = ictl
        if ipc == 0:
          self.ipc = '*na'
        else:
          self.ipc = ipc
        self.ebcdic_ccsid = iccsid
        self.pase_ccsid = pccsid

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
        data += " ebcdic_ccsid (" + str(self.ebcdic_ccsid) + ")"
        data += " pase_ccsid (" + str(self.pase_ccsid) + ")"
        return data

    def call(self, itool):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        return itoolkit.itoollib.xmlservice(itool.xml_in(),self.ctl,self.ipc,self.ebcdic_ccsid,self.pase_ccsid)


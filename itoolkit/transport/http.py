# -*- coding: utf-8 -*-
"""
XMLSERVICE http call

License: 
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.rest._HttpCall import *
  itransport = _HttpCall(url,user,password)
"""
import sys
import os
from ._base import _TransportBase

if sys.version_info >= (3,0):
    """
    urllib has been split up in Python 3.
    The urllib.urlencode() function is now urllib.parse.urlencode(),
    and the urllib.urlopen() function is now urllib.request.urlopen().
    """
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib import urlencode, urlopen

def connect(url, uid, pwd, rdb='*LOCAL', ctl='*here', ipc='*na', size=512000):
    return _HttpCall(url, uid, pwd, rdb, ctl, ipc, size)


class _HttpCall(_TransportBase):
    """
    Transport XMLSERVICE calls over standard HTTP rest.

    Args:
      url   (str): XMLSERVICE url (https://common1.frankeni.com:47700/cgi-bin/xmlcgi.pgm).
      uid   (str): Database user profile name
      pwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass) 
      rdb   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ctl   (str): optional - XMLSERVICE control ['*here','*sbmjob']
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42']
      size   (str): optional - XMLSERVICE expected max XML output size, required for DB2 

    Example:
      from itoolkit.rest._HttpCall import *
      itransport = _HttpCall(url,user,password)

    Returns:
      none
    """
    def __init__(self, url, uid, pwd, rdb='*LOCAL', ctl='*here', ipc='*na', size=512000):
        self.url = url
        self.uid = uid
        self.pwd = pwd
        self.rdb = rdb
        self.ctl = ctl
        self.ipc = ipc
        self.size = size

    def __str__(self):
        """Return trace driver data.

        Args:
          none

        Returns:
          initialization data
        """
        return "ctl ({}) ipc ({}) uid ({}) rdb ({}) size (%d) url ({})".format(
            self.ctl, self.ipc, self.uid, self.rdb, self.size, self.url)

    def execute(self, xml_or_toolkit):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        try:
            xml = xml_or_toolkit.xml_in()
        except AttributeError:
            xml = str(xml_or_toolkit)
        
        params = urlencode({
            'db2': self.rdb,
            'uid': self.uid,
            'pwd': self.pwd,
            'ipc': self.ipc,
            'ctl': self.ctl + " *cdata",
            'xmlin': xml,
            'xmlout': self.size
        })
        data = params.encode('utf-8')
        usock = urlopen(self.url, data)
        
        xml_out = usock.read()
        usock.close()
        return xml_out



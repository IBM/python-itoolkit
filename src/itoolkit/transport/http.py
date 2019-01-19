# -*- coding: utf-8 -*-
"""
XMLSERVICE http/rest/web call (Apache job)

License:
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Import:
  from itoolkit import *
  from itoolkit.transport import HttpTransport
  itransport = HttpTransport(url, user, password)
"""
from .base import XmlServiceTransport
import sys
import os
import urllib

if sys.version_info >= (3, 0):
    """
    urllib has been split up in Python 3.
    The urllib.urlencode() function is now urllib.parse.urlencode(),
    and the urllib.urlopen() function is now urllib.request.urlopen().
    """
    import urllib.request
    import urllib.parse

__all__ = [
    'HttpTransport'
]


class HttpTransport(XmlServiceTransport):
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
      from itoolkit.transport import HttpTransport
      itransport = HttpTransport(url,user,password)

    Returns:
      none
    """

    def __init__(self, iurl, iuid, ipwd=None, idb2=0, ictl=0, ipc=0, isiz=0):
        if ictl == 0:
            ictl = '*here *cdata'

        if ipc == 0:
            ipc = '*na'

        super(HttpTransport, self).__init__(ictl, ipc)
        self.trace_attrs.extend([
            'uid',
            'db2',
            'siz',
            'url'
        ])

        # manditory
        self.url = iurl
        self.uid = iuid
        # optional
        if ipwd == 0:
            self.pwd = os.environ['PASSWORD']
        else:
            self.pwd = ipwd
        if idb2 == 0:
            self.db2 = '*LOCAL'
        else:
            self.db2 = idb2
        if isiz == 0:
            self.siz = 512000
        else:
            self.siz = isiz

    def call(self, itool):
        """Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml
        """
        if sys.version_info >= (3, 0):
            """
            urllib has been split up in Python 3.
            The urllib.urlencode() function is now urllib.parse.urlencode(),
            and the urllib.urlopen() function is now urllib.request.urlopen().
            """
            params = urllib.parse.urlencode({
                'db2': self.db2,
                'uid': self.uid,
                'pwd': self.pwd,
                'ipc': self.ipc,
                'ctl': self.ctl + " *cdata",
                'xmlin': itool.xml_in(),
                'xmlout': self.siz
            })
            data = params.encode('utf-8')
            request = urllib.request.Request(self.url)
            usock = urllib.request.urlopen(request, data)
        else:
            params = urllib.urlencode({
                'db2': self.db2,
                'uid': self.uid,
                'pwd': self.pwd,
                'ipc': self.ipc,
                'ctl': self.ctl + " *cdata",
                'xmlin': itool.xml_in(),
                'xmlout': self.siz
            })
            usock = urllib.urlopen(self.url, params)
        xml_out = usock.read()
        usock.close()
        return xml_out

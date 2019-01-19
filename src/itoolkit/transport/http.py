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
# import inspect

__all__ = [
    'HttpTransport'
]


class HttpTransport(object):
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

    def __init__(self, iurl, iuid, ipwd=0, idb2=0, ictl=0, ipc=0, isiz=0):
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
        data += " url (" + str(self.url) + ")"
        return data

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

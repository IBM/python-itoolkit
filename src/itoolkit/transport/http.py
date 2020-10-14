# -*- coding: utf-8 -*-
from .base import XmlServiceTransport
import contextlib
import sys

if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib import urlencode, urlopen

__all__ = [
    'HttpTransport'
]


class HttpTransport(XmlServiceTransport):
    """Call XMLSERVICE using FastCGI endpoint

    For more information, refer to
    http://yips.idevcloud.com/wiki/index.php/XMLService/XMLSERVICEGeneric

    Args:
      url (str): XMLSERVICE FastCGI endpoint
            eg. https://example.com/cgi-bin/xmlcgi.pgm
      user (str): Database user profile name
      password (str, optional): Database password
      database (str, optional): Database name (RDB) to connect to
      **kwargs: Base transport options. See `XmlServiceTransport`.

    Example:
        >>> from itoolkit.transport import HttpTransport
        >>> endpoint = 'https://example.com/cgi-bin/xmlcgi.pgm'
        >>> transport = HttpTransport(endpoint, 'user', 'pass')
    """
    def __init__(self, url, user, password, database='*LOCAL', **kwargs):
        super(HttpTransport, self).__init__(**kwargs)
        self.trace_attrs.extend([
            'url',
            ('uid', 'user'),
            ('rdb', 'database'),
        ])

        self.url = url
        self.uid = user
        self.pwd = password
        self.db = database

    OUT_SIZE = 16 * 1000 * 1000

    def _call(self, tk):
        data = urlencode({
            'db2': self.db,
            'uid': self.uid,
            'pwd': self.pwd,
            'ipc': self.ipc,
            'ctl': self.ctl,
            'xmlin': tk.xml_in(),
            'xmlout': self.OUT_SIZE
        }).encode('utf-8')

        with contextlib.closing(urlopen(self.url, data)) as f:
            return f.read()

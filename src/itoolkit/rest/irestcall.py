# -*- coding: utf-8 -*-
import warnings
import os
from ..transport.http import HttpTransport


class iRestCall(HttpTransport): # noqa N801
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
      from itoolkit.rest.irestcall import *
      itransport = iRestCall(url,user,password)

    Returns:
      none
    """
    def __init__(self, iurl, iuid, ipwd=None, idb2=0, ictl=0, ipc=0, isiz=0):
        warnings.warn(
            "iRestCall is deprecated, "
            "use itoolkit.transport.HttpTransport instead",
            category=DeprecationWarning,
            stacklevel=2)

        if not ictl:
            ictl = '*here *cdata'

        if not ipc:
            ipc = '*na'

        if not ipwd:
            ipwd = os.environ['PASSWORD']

        if not idb2:
            idb2 = '*LOCAL'

        if isiz not in (0, self.OUT_SIZE):
            msg = "isiz is deprecated, changed to {}".format(self.OUT_SIZE)
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)

        super(iRestCall, self).__init__(url=iurl, user=iuid, password=ipwd,
                                        database=idb2, ctl=ictl, ipc=ipc)

    def call(self, itool):
        """Call XMLSERVICE with accumulated actions.

        Args:
          itool: An iToolkit object

        Returns:
          The XML returned from XMLSERVICE
        """
        return super(iRestCall, self).call(itool)

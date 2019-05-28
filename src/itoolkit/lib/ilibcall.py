# -*- coding: utf-8 -*-
import warnings
from ..transport.direct import DirectTransport


class iLibCall(DirectTransport): # noqa N801 gotta live with history
    """
    Transport XMLSERVICE direct job call (within job/process calls).

    Args:
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob']
      ipc    (str): optional - XMLSERVICE job route for *sbmjob '/tmp/myunique'
      iccsid (int): optional - XMLSERVICE EBCDIC CCSID (0 = default jobccsid)
      pccsid (int): optional - XMLSERVICE ASCII CCSID

    Returns:
      none
    """
    def __init__(self, ictl='*here *cdata', ipc='*na', iccsid=0, pccsid=1208):
        warnings.warn(
            "iLibCall is deprecated, "
            "use itoolkit.transport.DirectTransport instead",
            category=DeprecationWarning,
            stacklevel=2)

        if iccsid != 0:
            raise ValueError("iccsid must be 0 (job ccsid)")

        if pccsid != 1208:
            raise ValueError("pccsid must be 1208 (UTF-8)")

        super(iLibCall, self).__init__(ctl=ictl, ipc=ipc)

    def call(self, itool):
        """Call XMLSERVICE with accumulated actions.

        Args:
          itool: An iToolkit object

        Returns:
          The XML returned from XMLSERVICE
        """
        return super(iLibCall, self).call(itool)

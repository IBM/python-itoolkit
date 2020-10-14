# -*- coding: utf-8 -*-
import sys
from .base import XmlServiceTransport

try:
    # _direct will raise an ImportError when it is running on an unsupported
    # platform. This is fine, we check for this in DirectTransport.call
    from . import _direct
except ImportError:
    pass

__all__ = [
    'DirectTransport'
]


class DirectTransport(XmlServiceTransport):
    """Call XMLSERVICE directly in-process using _ILECALL

    Args:
      **kwargs: Base transport options. See `XmlServiceTransport`.

    Example:
        >>> from itoolkit.transport import DirectTransport
        >>> transport = DirectTransport()
    """
    def __init__(self, **kwargs):
        super(DirectTransport, self).__init__(**kwargs)

    def _call(self, tk):
        try:
            data = _direct.xmlservice(tk.xml_in(), self.ctl, self.ipc)

            if len(data) == 0:
                # Older versions of XMLSERVICE did not work correctly when
                # called directly from a 64-bit PASE application and output is
                # left empty. We check for that here and suggest they install
                # the updated version.
                raise RuntimeError(
                    "No data returned from XMLSERVICE. "
                    "This could be a bug present in XMLSERVICE prior to 2.0.1. "
                    "Perhaps you need to apply PTF SI70667, SI70668 or SI70669?"
                )

            if sys.version_info >= (3, 0):
                return data.decode('utf-8')
            else:
                return data
        except NameError:
            # When we drop support for Python 2:
            # raise RuntimeError("Not supported on this platform") from None
            raise RuntimeError("Not supported on this platform")

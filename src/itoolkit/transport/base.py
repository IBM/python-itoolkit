from ..errors import TransportClosedException


class XmlServiceTransport(object):
    """XMLSERVICE transport base class

    Args:
      ctl (str): XMLSERVICE control options, see
        http://yips.idevcloud.com/wiki/index.php/XMLService/XMLSERVICEQuick#ctl
      ipc (str): An XMLSERVICE ipc key for stateful conections, see
        http://yips.idevcloud.com/wiki/index.php/XMLService/XMLSERVICEConnect
    """
    def __init__(self, ctl="*here *cdata", ipc="*na"):
        self.ipc = ipc
        self.ctl = ctl

        self.trace_attrs = ["ipc", "ctl"]
        self._is_open = True

    def __del__(self):
        self.close()

    def trace_data(self):
        output = ""

        for i in self.trace_attrs:
            if isinstance(i, tuple):
                trace, attr = i
            else:
                trace = attr = i

            output += " {}({})".format(trace, getattr(self, attr))

        return output

    def call(self, tk):
        """Call XMLSERVICE with accumulated actions

        Args:
          tk (iToolKit): An iToolkit object

        Returns:
          str: The XML returned from XMLSERVICE
        """
        self._ensure_open()

        return self._call(tk)

    def _call(self, tk):
        """Called by :py:func:`call`. This should be overridden by subclasses
        to the call function instead of overriding :py:func:`call` directly.
        """
        raise NotImplementedError

    def _ensure_open(self):
        """This should be called by any subclass function which uses
        resources which may have been released when `close` is called."""
        if not self._is_open:
            raise TransportClosedException()

    def close(self):
        """Close the connection now rather than when :py:func:`__del__` is
        called.

        The transport will be unusable from this point forward and a
        :py:exc:`TransportClosedException` exception will be raised if any
        operation is attempted with the transport.
        """
        self._close()
        self._is_open = False

    def _close(self):
        """Called by `close`. This should be overridden by subclasses to close
        any resources specific to that implementation."""
        pass

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
        raise NotImplementedError

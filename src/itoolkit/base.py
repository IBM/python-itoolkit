import xml.dom.minidom

class iBase(object): # noqa N801
    """IBM i XMLSERVICE call addable operation(s).

    Args:
      iopt (dict): user options (see descendents)
      idft (dict): default options (see descendents)

    Example:
      Calling a CL command and shell script::

        itransport = DirectTransport()
        itool = iToolKit()
        itool.add(iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE)'))
        itool.add(iSh('ps', 'ps -ef'))
        ... so on ...
        itool.call(itransport)

    Notes:
      iopt  (dict): XMLSERVICE elements, attributes and values
                    '_tag' - element <x>
                    'value' - value <x>value</x>
                    'id' - attribute <x var='ikey'>
                    'children' - iBase children
                    ... many more idft + iopt ...
                    'error' - <x 'error'='fast'>
    """

    def __init__(self, iopt={}, idft={}):
        # xml defaults
        self.opt = idft.copy()
        self.opt.update(iopt)

        # my children objects
        self.opt['_children'] = []

    def add(self, obj):
        """Additional mini dom xml child nodes.

        Args:
          obj (iBase) : additional child object

        Example:
          Adding a program::

            itool = iToolKit()
            itool.add(
              iPgm('zzcall','ZZCALL')             <--- child of iToolkit
              .addParm(iData('INCHARA','1a','a')) <--- child of iPgm
            )
        """
        self.opt['_children'].append(obj)

    def xml_in(self):
        """Return XML string of collected mini dom xml child nodes.

        Returns:
          XML (str)
        """
        return self.make().toxml()

    def make(self, doc=None):
        """Assemble coherent mini dom xml, including child nodes.

        Returns:
          xml.dom.minidom (obj)
        """

        if not doc:
            doc = xml.dom.minidom.Document()

        return self._make(doc)

    def _make(self, doc):
        tag = doc.createElement(self.opt['_tag'])
        tag.setAttribute('var', self.opt['_id'])

        for attr, value in self.opt.items():
            if not attr.startswith('_'):
                tag.setAttribute(attr, str(value))

        if len(self.opt['_value']):
            value = doc.createCDATASection(self.opt['_value'])
            tag.appendChild(value)

        for child in self.opt['_children']:
            tag.appendChild(child.make(doc))

        return tag


class iXml(iBase): # noqa N801
    """
    IBM i XMLSERVICE raw xml input.

    Args:
      ixml  (str): custom XML for XMLSERVICE operation.

    Example:
      iXml("<cmd>CHGLIBL LIBL(XMLSERVICE)</cmd>")
      iXml("<sh>ls /tmp</sh>")

    Returns:
      iXml (obj)

    Notes:
      Not commonly used, but ok when other classes fall short.
    """

    def __init__(self, ixml):
        super().__init__()
        self.xml_body = ixml

    def add(self, obj):
        """add input not allowed.

        Returns:
          raise except
        """
        raise

    def _make(self, _doc):
        """Assemble coherent mini dom xml.

        Returns:
          xml.dom.minidom (obj)
        """
        try:
            node = xml.dom.minidom.parseString(self.xml_body).firstChild
        except xml.parsers.expat.ExpatError as e:
            e.args += (self.xml_body,)
            raise
        return node

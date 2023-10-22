# Copyright contributors to the python-itoolkit project 
# SPDX-License-Identifier: MIT
import xml.dom.minidom
import re
import sys
import time
import logging
import warnings


class iToolKit: # noqa N801
    """
    Main iToolKit XMLSERVICE collector and output parser.

    Args:
      iparm (num): include xml node parm output (0-no, 1-yes).
      iret  (num): include xml node return output (0-no, 1-yes).
      ids   (num): include xml node ds output (0-no, 1-yes).
      irow  (num): include xml node row output (0-no, 1-yes).

    Returns:
      iToolKit (obj)
    """

    def __init__(self, iparm=0, iret=0, ids=1, irow=1):
        # XMLSERVICE
        self.data_keys = ["cmd", "pgm", "sh", "sql"]
        self.data_vals = [
            "cmd",
            "sh",
            "data",
            "success",
            "error",
            "xmlhint",
            "jobipcskey",
            "jobname",
            "jobuser",
            "jobnbr",
            "curuser",
            "ccsid",
            "dftccsid",
            "paseccsid",
            "joblog",
            "jobipc",
            "syslibl",
            "usrlibl",
            "version",
            "jobcpf"]
        if iparm:
            self.data_keys.append("parm")
            self.data_vals.append("parm")
        if iret:
            self.data_keys.append("return")
        if irow:
            self.data_keys.append("row")
            self.data_vals.append("row")
        if ids:
            self.data_keys.append("ds")

        self.input = []
        self.domo = ""

        self.logger = logging.getLogger('itoolkit-trace')
        self.trace_handler = None

    def clear(self):
        """Clear collecting child objects.

        Notes:
          <?xml version='1.0'?>
          <xmlservice>
        """
        # XMLSERVICE
        self.input = []
        self.domo = ""

    def add(self, obj):
        """Add additional child object.

        Args:
          obj

        Notes:
          <?xml version='1.0'?>
          <xmlservice>
        """
        self.input.append(obj)

    def xml_in(self):
        """return raw xml input.

        Returns:
          xml
        """
        doc = xml.dom.minidom.Document()

        root = doc.createElement("xmlservice")
        doc.appendChild(root)

        for item in self.input:
            root.appendChild(item._make(doc))

        return doc.toxml()

    def xml_out(self):
        """return raw xml output.

        Returns:
          xml
        """
        domo = self._dom_out()
        return domo.toxml()

    def list_out(self, ikey=-1):
        """return list output.

        Args:
          ikey  (num): select list from index [[0],[1],,,,].

        Returns:
          list [value]
        """
        output = []
        domo = self._dom_out()
        self._parseXmlList(domo, output)
        if ikey > -1:
            try:
                return output[ikey]
            except IndexError:
                output[ikey] = output
                return output[ikey]
        else:
            return output

    def dict_out(self, ikey=0):
        """return dict output.

        Args:
          ikey  (str): select 'key' from {'key':'value'}.

        Returns:
          dict {'key':'value'}
        """
        self.unq = 0
        output = {}
        domo = self._dom_out()
        self._parseXmlDict(domo, output)
        if isinstance(ikey, str):
            try:
                return output[ikey]
            except KeyError:
                output[ikey] = {'error': output}
                return output[ikey]
        else:
            return output

    def hybrid_out(self, ikey=0):
        """return hybrid output.

        Args:
          ikey  (str): select 'key' from {'key':'value'}.

        Returns:
          hybrid {key:{'data':[list]}}
        """
        self.unq = 0
        output = {}
        domo = self._dom_out()
        self._parseXmlHybrid(domo, output)
        if isinstance(ikey, str):
            try:
                return output[ikey]
            except KeyError:
                output[ikey] = {'error': output}
                return output[ikey]
        else:
            return output

    def trace_open(self, iname='*terminal'):
        r"""Open trace file.

        If ``iname`` is "\*terminal", trace will output to ``sys.stdout``.
        Otherwise, a file path with the format /tmp/python_toolkit_(iname).log
        is used to open a trace file in append mode.

        Args:
          iname  (str): Name of trace file or "\*terminal" for ``sys.stdout``

        .. versionadded:: 1.2
        .. deprecated:: 2.0
          See :ref:`Tracing <tracing>`.
        """
        warnings.warn(
                "trace_open is deprecated, use the logging module instead",
                category=DeprecationWarning,
                stacklevel=2)

        self.trace_close()

        if '*' in iname:
            self.trace_handler = logging.StreamHandler(sys.stdout)
        else:
            path = f'/tmp/python_toolkit_{iname}.log'
            self.trace_handler = logging.FileHandler(path)

        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.trace_handler)

    def trace_close(self):
        """End trace and close trace file.

        .. versionadded:: 1.2
        .. deprecated:: 2.0
          See :ref:`Tracing <tracing>`.
        """
        warnings.warn("trace_close is deprecated", category=DeprecationWarning,
                      stacklevel=2)

        if not self.trace_handler:
            return

        self.logger.removeHandler(self.trace_handler)
        try:
            self.trace_handler.close()
        except AttributeError:
            # logging.StreamHandler doesn't support close
            pass

        self.trace_handler = None

    def call(self, itrans):
        """Call xmlservice with accumulated input XML.

        Args:
          itrans (obj): XMLSERVICE transport object

        Raises:
          itoolkit.transport.TransportClosedError: If the transport has been
            closed.
        """
        self.logger.info('***********************')
        self.logger.info('control ' + time.strftime("%c"))
        self.logger.info(itrans.trace_data())
        self.logger.info('input ' + time.strftime("%c"))
        self.logger.info(self.xml_in())

        # step 1 -- make call
        step = 1
        xml_out = itrans.call(self)
        if not (xml_out and xml_out.strip()):
            xml_out = """<?xml version='1.0'?>
<xmlservice>
<error>*NODATA</error>
</xmlservice>"""
        # step 1 -- parse return
        try:
            self.logger.info('output ' + time.strftime("%c"))
            self.logger.info(xml_out)
            domo = xml.dom.minidom.parseString(xml_out)
        except Exception:
            step = 2
        # step 2 -- bad parse, try modify bad output
        if step == 2:
            try:
                self.logger.info('parse (fail) ' + time.strftime("%c"))

                def to_printable(c):
                    s = chr(c)
                    return s if s.isprintable() else '.'

                data = xml_out.encode()
                for i in range(0, len(data), 16):
                    chunk = data[i:i+16]

                    hex = chunk.hex().ljust(32)
                    text = "".join([to_printable(_) for _ in chunk])
                    self.logger.info(f'{hex} {text}')

                clean1 = re.sub(r'[\x00-\x1F\x3C\x3E]', ' ', xml_out)
                clean = re.sub(' +', ' ', clean1)
                xml_out2 = """<?xml version='1.0'?>
<xmlservice>
<error>*BADPARSE</error>
<error><![CDATA[{}]]></error>
</xmlservice>""".format(clean)
                domo = xml.dom.minidom.parseString(xml_out2)
            except Exception:
                step = 3
        # step 3 -- horrible parse, give up on output
        if step == 3:
            xml_out2 = """<?xml version='1.0'?>
<xmlservice>
<error>*NOPARSE</error>
</xmlservice>"""
            domo = xml.dom.minidom.parseString(xml_out2)
        self.logger.info(
                'parse step: ' +
                str(step) +
                ' (1-ok, 2-*BADPARSE, 3-*NOPARSE)')
        self.domo = domo

    def _dom_out(self):
        """return xmlservice dom output.

        Returns:
          xml.dom
        """
        if self.domo == "" or self.domo is None:
            # something very bad happened
            xmlblank = "<?xml version='1.0'?>\n"
            xmlblank += "<xmlservice>\n"
            xmlblank += "<error>no output</error>\n"
            xmlblank += "<xmlhint><![CDATA["
            for v in self.input:
                xmlblank += v.xml_in().replace("<", " ").replace(">", " ")
            xmlblank += "]]></xmlhint>\n"
            xmlblank += "</xmlservice>"
            self.domo = xml.dom.minidom.parseString(xmlblank)
        return self.domo

    def _parseXmlList(self, parent, values): # noqa N802
        """return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate list []

        Returns:
          list [value]
        """
        for child in parent.childNodes:
            if child.nodeType in (child.TEXT_NODE, child.CDATA_SECTION_NODE):
                if child.parentNode.tagName in self.data_vals \
                   and child.nodeValue != "\n":
                    values.append(child.nodeValue)
            elif child.nodeType == xml.dom.Node.ELEMENT_NODE:
                if child.tagName in self.data_keys:
                    child_values = []  # values [v,v,...]
                    values.append(child_values)
                    self._parseXmlList(child, child_values)
                else:
                    # make sure one empty data value (1.1)
                    if child.tagName in self.data_vals and not(
                            child.childNodes):
                        child.appendChild(self.domo.createTextNode(""))
                    self._parseXmlList(child, values)

    def _parseXmlDict(self, parent, values): # noqa N802
        """return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate dict{}

        Returns:
          dict {'key':'value'}
        """
        for child in parent.childNodes:
            if child.nodeType in (child.TEXT_NODE, child.CDATA_SECTION_NODE):
                if child.parentNode.tagName in self.data_vals \
                   and child.nodeValue != "\n":
                    var = child.parentNode.getAttribute('var')
                    if var == "":
                        var = child.parentNode.getAttribute('desc')
                    if var == "":
                        var = child.parentNode.tagName
                    # special for sql parms
                    if child.parentNode.tagName in 'parm':
                        var = "data"
                    myvar = var
                    while var in values:
                        self.unq += 1
                        var = myvar + str(self.unq)
                    values[var] = child.nodeValue
            elif child.nodeType == xml.dom.Node.ELEMENT_NODE:
                if child.tagName in self.data_keys:
                    var = child.getAttribute('var')
                    if var == "":
                        var = child.tagName
                    # key was already in values
                    # becomes list of same name
                    child_values = {}
                    if var in values:
                        old = values[var]
                        if isinstance(old, list):
                            old.append(child_values)
                        else:
                            values[var] = []
                            values[var].append(old)
                            values[var].append(child_values)
                    else:
                        values[var] = child_values
                    self._parseXmlDict(child, child_values)
                else:
                    # make sure one empty data value (1.1)
                    if child.tagName in self.data_vals and not(
                            child.childNodes):
                        child.appendChild(self.domo.createTextNode(""))
                    self._parseXmlDict(child, values)

    def _parseXmlHybrid(self, parent, values): # noqa N802
        """return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate hybrid{}

        Returns:
          hybrid {key:{'data':[list]}}
        """
        for child in parent.childNodes:
            if child.nodeType in (child.TEXT_NODE, child.CDATA_SECTION_NODE):
                if child.parentNode.tagName in self.data_vals \
                   and child.nodeValue != "\n":
                    if 'data' not in values:
                        values['data'] = []
                    values['data'].append(child.nodeValue)
            elif child.nodeType == xml.dom.Node.ELEMENT_NODE:
                if child.tagName in self.data_keys:
                    var = child.getAttribute('var')
                    if var == "":
                        var = child.tagName
                    # key was already in values
                    # becomes list of same name
                    child_values = {}
                    if var in values:
                        old = values[var]
                        if isinstance(old, list):
                            old.append(child_values)
                        else:
                            values[var] = []
                            values[var].append(old)
                            values[var].append(child_values)
                    else:
                        values[var] = child_values
                    self._parseXmlHybrid(child, child_values)
                else:
                    # make sure one empty data value (1.1)
                    if child.tagName in self.data_vals and not(
                            child.childNodes):
                        child.appendChild(self.domo.createTextNode(""))
                    self._parseXmlHybrid(child, values)

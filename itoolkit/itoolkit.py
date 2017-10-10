# -*- coding: utf-8 -*-
"""
IBM i python toolkit. 

The toolkit runs both local and remote to IBM i using iDB2Call or iRestCall. 
However, class iLibCall process local executes will only work on IBM i (similar to IBM i CL).

Transport classes:
  class iLibCall:             Transport XMLSERVICE direct job execute (within job/process executes).
  class iDB2Call:             Transport XMLSERVICE executes over DB2 connection.
  class iRestCall:            Transport XMLSERVICE executes over standard HTTP rest.

XMLSERVICE classes:
  Base:
  class iToolKit:             Main iToolKit XMLSERVICE collector and output parser.
  class _Base:                IBM i XMLSERVICE execute addable operation(s).

  *CMDs:
  class iCmd(_Base):          IBM i XMLSERVICE execute *CMD not returning *OUTPUT.

  PASE:
  class iSh(_Base):           IBM i XMLSERVICE execute 5250 *CMD returning *OUTPUT.
  class iCmd5250(iSh):        IBM i XMLSERVICE execute PASE utilities.

  *PGM or *SRVPGM:
  class iPgm (_Base):         IBM i XMLSERVICE execute *PGM.
  class iSrvPgm (iPgm):       IBM i XMLSERVICE execute *SRVPGM.
  class include_param (_Base):        Parameter child node for iPgm or iSrvPgm
  class include_return (_Base):         Return structure child node for iSrvPgm
  class inlude_ds (_Base):          Data structure child node for iPgm, iSrvPgm,
                              or nested inlude_ds data structures.
  class iData (_Base):        Data value child node for iPgm, iSrvPgm,
                              or inlude_ds data structures.

  DB2:
  class iSqlQuery (_Base):    IBM i XMLSERVICE execute DB2 execute direct SQL statment.
  class iSqlPrepare (_Base):  IBM i XMLSERVICE execute DB2 prepare SQL statment.
  class iSqlExecute (_Base):  IBM i XMLSERVICE execute execute a DB2 prepare SQL statment.
  class iSqlFetch (_Base):    IBM i XMLSERVICE execute DB2 fetch results/rows of SQL statment.
  class iSqlParm (_Base):     Parameter child node for iSqlExecute.
  class iSqlFree (_Base):     IBM i XMLSERVICE execute DB2 free open handles.

  Anything (XMLSERVICE XML, if no class exists):
  class iXml(_Base):          IBM i XMLSERVICE raw xml input.

Import:
  1) XMLSERVICE direct execute (current job) - local only
  from itoolkit import *
  from itoolkit.lib.ilibcall import *
  transportport = iLibCall()

  2) XMLSERVICE db2 execute (QSQSRVR job) - local/remote
  from itoolkit import *
  from itoolkit.db2.idb2call import *
  transportport = iDB2Call(user,password)
  -- or -
  conn = ibm_db.connect(database, user, password)
  transportport = iDB2Call(conn)

  3) XMLSERVICE http/rest/web execute (Apache job) - local/remote
  from itoolkit import *
  from itoolkit.rest.irestcall import *
  transportport = iRestCall(url,user,password)

Samples (itoolkit/sample):
  > cd /QOpenSys/QIBM/ProdData/OPS/Python3.4/lib/python3.4/site-packages/itoolkit/sample
  > python3 icmd5250_dspsyssts.py

  > cd /QOpenSys/QIBM/ProdData/OPS/Python2.7/lib/python2.7/site-packages/itoolkit/sample
  > python2 icmd5250_dspsyssts.py

Install:
  =====
  IBM pythons (PTF):
  =====
  pip3 uninstall itoolkit
  pip3 install dist/itoolkit*34m-os400*.whl
  pip2 uninstall itoolkit
  pip2 install dist/itoolkit*27m-os400*.whl
  ======
  perzl pythons
  ======
  rm  -R /opt/freeware/lib/python2.6/site-packages/itoolkit*
  easy_install dist/itoolkit*2.6-os400*.egg
  rm  -R /opt/freeware/lib/python2.7/site-packages/itoolkit*
  easy_install-2.7 dist/itoolkit*2.7-os400*.egg
  ======
  laptop/remote pythons
  ======
  pip uninstall itoolkit
  pip install dist/itoolkit-lite*py2-none*.whl
  -- or --
  easy_install dist/itoolkit-lite*2.7.egg

Configure:
  Requires XMLSERVICE library installed.
  1) IBM i DGO PTFs ship QXMLSERV library (Apache PTFs)
  -- or --
  2) see following link installation 
     http://yips.idevcloud.com/wiki/index.php/XMLService/XMLSERVICE
     (use crtxml for XMLSERVICE library)

Environment variables (optional):
  export XMLSERVICE=QXMLSERV  (default)
  -- or --
  export XMLSERVICE=XMLSERVICE
  -- or --
  export XMLSERVICE=ZENDSVR6
  -- so on --

License: 
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Links:
  https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/Python

"""
import sys
import os
import re
import time
import math
import abc
import struct
import datetime

from collections import OrderedDict
#from xml.dom.minidom import parseString
#from xml.dom import Node
from io import StringIO, BytesIO

from xml.etree.ElementTree import fromstring, ElementTree

from uuid import uuid4
# import inspect


if sys.version_info >= (3,0):
    def _is_string(obj):
        return isinstance(obj, str)
else:
    def _is_string(obj):
        return isinstance(obj, basestring) or isinstance(obj, unicode)

def _ensure_key_is_string(key):
    if not _is_string(key):
        raise ValueError("Key must be a string type")

class _Base:
    """
    IBM i XMLSERVICE execute addable operation(s).

      Args:
        iopt (dict): user options (see descendents)
        idft (dict): default options (see descendents)

      Example:
        transportport = iLibCall()
        itool = iToolKit()
        itool.add(iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE)'))
        itool.add(iSh('ps', 'ps -ef'))
        ... so on ...
        itool.execute(transportport)

      Returns:
        _Base (obj)

      Notes:
        iopt  (dict): XMLSERVICE elements, attributes and values
                      'k' - element <x>
                      'v' - value <x>value</x>
                      'i' - attribute <x var='key'>
                      'c' - _Base children
                      ... many more idft + iopt ...
                      'error' - <x 'error'='fast'>
    """
    def __init__(self, type, value=None, attributes=None):
        self.type = type
        self.value = value
        self.attributes = attributes
        self.success = False
        self._data = ""
        self._error = {}

    #def add(self, obj):
        #"""Additional mini dom xml child nodes.

        #Args:
          #obj (_Base) : additional child object 

        #Example:
          #itool = iToolKit()
          #itool.add(
            #iPgm('zzexecute','ZZexecute')             <--- child of iToolkit
            #.addParm(iData('INCHARA','1a','a')) <--- child of iPgm 
            #)

        #Returns:
          #(void)
        #"""
        #self.opt['c'].append(obj)


    def xml_in(self, key):
        """Return XML string of collected mini dom xml child nodes.

        Args:
          none

        Returns:
          XML (str)
        """
        if callable(value):
            value = self.value()
        else:
            value = self.value
            
        return "<{0} var='{1}' {2}>{3}</{0}>".format(
                self.type,
                key,
                " ".join([ "{}='{}'".format(k,v) for k,v in self.attributes.items()]),
                "" if value is None else '<![CDATA[{}]]>'.format(value))

    def make(self, key):
        return fromstring(self.xml_in(key))
    
    @abc.abstractmethod
    def _parse(self, node):
        """Should parse a node and set the flags"""
    
    @staticmethod
    def _parse_error(parent):
        error = {}
        
        for node in parent:
            if node.tag == 'error' and len(node) > 0:
                continue
            
            if node.tag == 'jobinfo':
                error['jobinfo'] = _Base._parse_error(node)
            else:
                error[node.tag] = node.text
                
        return error
    
    def succeeded(self):
        return self.success
    
    def data(self):
        return self._data
    
    def error_info(self):
        return self._error
        
    def old_make(self):
        """Assemble coherent mini dom xml, including child nodes.

        Args:
          none

        Returns:
          xml.dom.minidom (obj)
        """
        # XMLSERVICE
        xml = ""
        if 'j' in self.opt:
            xml += "<{} var='{}'>\n".format(self.opt['j'], self.opt['i'])
        
        attrs = " ".join([ "{}='{}'".format(k,v) for k,v in self.opt.items() if len(k) > 1])
        xml += "<{} var='{}' {}>".format(self.opt['k'], self.opt['i'], attrs)
        
        if 'v' in self.opt:
            xml += '<![CDATA[{}]]>'.format(self.opt['v'])
        
        xml += "</{}>\n".format(self.opt['k'])
        
        if 'j' in self.opt:
            xml += "</{}>\n".format(self.opt['j'])
        
        # build my children
        parent = fromstring(xml)
        is_sql = parent.tag == "sql"
        
        for obj in self.opt['c']:
            if is_sql and isinstance(obj, iSqlParm):
                parent.childNodes[1].appendChild(obj.make())
            else:
                parent.appendChild(obj.make())
        
        return parent

class CLCommand(_Base):
    """
    IBM i XMLSERVICE execute *CMD not returning *OUTPUT.

    Args:
      key  (str): XML <key>...operation ...</key> for parsing output.
      icmd  (str): IBM i command no output (see 5250 command prompt).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'}   : optional - XMLSERVICE error choice {'error':'fast'}
        {'exec':cmd|system|rexx'} : optional - XMLSERVICE command execute choice {'exec':'cmd'}
                                                              RTVJOBA CCSID(?N)      {'exec':'rex'}
    Example:
      iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE) CURLIB(XMLSERVICE)')
      iCmd('rtvjoba', 'RTVJOBA CCSID(?N) OUTQ(?)')

    Returns:
      iCmd (obj)

    Notes:
      Special commands returning output parameters are allowed.
       (?)  - indicate string return
       (?N) - indicate numeric return

      <cmd [exec='cmd|system|rexx'                        (default exec='cmd')
            hex='on' before='cc1/cc2/cc3/cc4' after='cc4/cc3/cc2/cc1'  (1.6.8)
            error='on|off|fast'                                        (1.7.6)
            ]>IBM i command</cmd>
    """
    def _need_rexx(command):
        # FIXME: This will mess up if you have a '?' inside a string parameter
        return "?" in command
    
    def __init__(self, command, use_rexx=None, on_error='fast'):
        if use_rexx is None:
            use_rexx = CLCommand._need_rexx(command)

        method = 'rexx' if use_rexx else 'cmd'
        
        super().__init__('cmd', command, {'exec': method, 'error': on_error})
    
    def _parse(self, node):
        self.success = False
        self._data = {}
        self._error = {}
        
        assert len(node) > 0
        for child in node:
            if child.tag == 'success':
                self.success = True
            if child.tag == 'error':
                self.success = False
                self._error = self._parse_error(node)
            elif child.tag == 'row':
                # We only expect one data node inside the row node
                assert len(child) == 1
                
                data_node = child[0]
                assert data_node.tag == 'data'
                
                key = data_node.attrib['desc']
                value = data_node.text
                
                self._data[key] = value
        
        # If the command did not return any data (exec=cmd never do, and
        # rexx commands without output parameters do not), there's no point
        # returning an empty dict, just set it to None
        # TODO: Should we do this?
        if len(self._data) == 0:
            self._data = None

class ShellCall(_Base):
    """
    IBM i XMLSERVICE call PASE utilities.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i PASE script/utility (see call qp2term).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'}  : optional - XMLSERVICE error choice {'error':'fast'}
        {'row':'on|off'}         : optional - XMLSERVICE <row>line output</row> choice {'row':'off'}

    Example:
      iSh('ls /home/xml/master | grep -i xml')

    Returns:
      iSh (obj)

    Notes:
      XMLSERVICE perfoms standard PASE shell popen calls,
      therefore, additional job will be forked,
      utilities will be exec'd, and stdout will
      be collected to be returned.

      Please note, this is a relatively slow operation,
      use sparingly on high volume web sites.   

      <sh [rows='on|off' 
           hex='on' before='cc1/cc2/cc3/cc4' after='cc4/cc3/cc2/cc1' (1.7.4)
           error='on|off|fast'                                       (1.7.6)
           ]>(PASE utility)</sh>
    """
    #def __init__(self, ikey, icmd, iopt={}):
        ## parent class
        #iBase.__init__(self,iopt, {'i':ikey,'k':'sh','v':icmd, 'error':'fast'})
        
    def __init__(self, command, on_error='fast'):
        super().__init__('sh', command, {'error': on_error})
    
    def _parse(self, node):
        # No way to detect whether the command succeeded or not
        self.success = True
        self._error = {}
        self._data = node.text
        
class CLCommandOutput(ShellCall):
    """
    IBM i XMLSERVICE call PASE utilities.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i PASE script/utility (see call qp2term).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'}  : optional - XMLSERVICE error choice {'error':'fast'}
        {'row':'on|off'}         : optional - XMLSERVICE <row>line output</row> choice {'row':'off'}

    Example:
      iSh('ls /home/xml/master | grep -i xml')

    Returns:
      iSh (obj)

    Notes:
      XMLSERVICE perfoms standard PASE shell popen calls,
      therefore, additional job will be forked,
      utilities will be exec'd, and stdout will
      be collected to be returned.

      Please note, this is a relatively slow operation,
      use sparingly on high volume web sites.   

      <sh [rows='on|off' 
           hex='on' before='cc1/cc2/cc3/cc4' after='cc4/cc3/cc2/cc1' (1.7.4)
           error='on|off|fast'                                       (1.7.6)
           ]>(PASE utility)</sh>
    """
    #def __init__(self, ikey, icmd, iopt={}):
        ## parent class
        #iBase.__init__(self,iopt, {'i':ikey,'k':'sh','v':icmd, 'error':'fast'})
        
    def __init__(self, command, on_error='fast'):
        sh_command = '/QOpenSys/usr/bin/system "{}"'.format(command)
        super().__init__(sh_command, on_error)

class DataFieldBase():
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def _encode(self):
        pass
    
    @abc.abstractmethod
    def _decode(self):
        pass
    
    def encode(self):
        str(value)
    
    def _xml(self, key):
        if value is None:
            value = ''
        elif self._hex and not self._value_is_hex_encoded:
            value = self._encode()
        else:
            value = self.encode()
        
        return "<data var='{1}' {2}>{3}</data>".format(
                key,
                " ".join([ "{}='{}'".format(k,v) for k,v in self._attrs.items()]),
                "" if not value else '<![CDATA[{}]]>'.format(self._value))

class _TypeBase():
    @classmethod
    def match(cls, value):
        return False
    
    @classmethod
    def create(cls, *args, **kwargs):
        return None
    
    def __init__(self, type):
        self._type = type
        self._varying = False
        self._always_hex = False
    
    def type_string(self):
        return self._type
    
    def varying(self):
        return self._varying
    
    def encode(self, value):
        return str(value)
    
    def decode(self, value):
        return value
    
class IntType(_TypeBase):
    def __init__(self), size, signed):
        digits = {
            1: '3',
            2: '5',
            4: '10',
            8: '20',
        }[size]
        letter = 'i' if signed else 'u'
        super().__init(digits + letter + '0')
        
        self._size = size
        self._signed = signed
    
    def __ensure_range(self, value):
        bits = 8 * self._size
        
        if self._signed:
            min_val = 0
            max_val = 2**bits
        else:
            bits -= 1
            min_val = -2**bits
            max_val =  2**bits - 1
            
        if value < min_val or value > max_val:
            raise ValueError("value not in range")
    
    __pack_mapping = {
        1: ('B', 'b'),
        2: ('H', 'h'),
        4: ('I', 'i'),
        8: ('Q', 'q'),
    }
    #def _encode_hex(self, value):
        #self.__ensure_range(value)
        #fmt = '>' + __pack_mapping[self._size][int(self._signed)]
        #data = struct.pack(fmt, value)
        #return data.encode('hex')
    
    #def _decode_hex(self, hex):
        #self.__ensure_range(value)
        #data = hex.decode('hex')
        #fmt = '>' + __pack_mapping[self._size][int(self._signed)]
        #return struct.unpack(fmt, data)[0]
    
    def encode(self, value):
        self.__ensure_range(value)
        return str(value)
    
    #@classmethod
    #def match(cls, value):
        #return False

class FloatType(_TypeBase):
    def __init__(self, is_double):
        super().__init__('8f4' if is_double else '4f2')
        self._double = is_double
    
class ZonedType(_TypeBase):
    def __init__(self, precision, scale):
        super().__init__("{}s{}".format(precision, scale))
    
class PackedType(_TypeBase):
    def __init__(self, precision, scale):
        super().__init__("{}p{}".format(precision, scale))
    
class BinaryType(_TypeBase):
    def __init__(self, length):
        super().__init__(int(length) + "b")
        self._always_hex = True
        
    def _encode_hex(self, value):
        return value.encode('hex')
    
    def _decode_hex(self, hex):
        return hex.decode('hex')
        
class HoleType(_TypeBase):
    def __init__(self, length):
        super().__init__(int(length) + "h")
        
    def _encode_hex(self, value):
        return None
    
    def _decode_hex(self, hex):
        return None
        
    def encode(self, value):
        return None
    
    def decode(self, value):
        return None
    
class CharType(_TypeBase):
    def __init__(self, length, varying=False):
        super().__init__(int(length) + "a")
        self._varying = varying
        
class BooleanType(CharType):
    def __init__(self):
        super().__init__(4)
        
    def encode(self, value):
        # TODO: Verify this is right
        return '*YES' if value else '*NO '
    
    def decode(self, value):
        return True if value == '*YES' else False
        
class TimeType(CharType):
    def __init__(self):
        super().__init__(8)
        
    _format = '%H.%M.%S'
    def encode(self, value):
        if isinstance(value, datetime.time):
            return value.strftime(self._format)
        else:
            return str(value)
        
    def encode(self, value):
        return datetime.strptime(self._format).time()
        
class DateType(CharType):
    def __init__(self):
        super().__init__(10)
        
    _format = '%Y-%m-%d'
    def encode(self, value):
        if isinstance(value, datetime.date):
            return value.strftime(self._format)
        else:
            return str(value)
        
    def encode(self, value):
        return datetime.strptime(self._format).date()
        
class TimestampType(CharType):
    def __init__(self):
        super().__init__(26)
        
    _format = '%Y-%m-%d-%H.%M.%S.%f'
    def encode(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime(self._format)
        else:
            return str(value)
        
    def encode(self, value):
        return datetime.strptime(self._format)

    
class DataField():
    _supported_types = (
        IntType,
        FloatType,
        CharType,
        ZonedType,
        PackedType,
        BinaryType,
        HoleType,
        BooleanType,
        TimeType,
        DateType,
        TimestampType,
    )
    def __init__(self, type, value=None, varying=False, array_count=None, **kwargs):
        self._type = None
        
        for cls in self._supported_types:
            if cls.match(type):
                self._type = cls.create(type, varying)
                break
        
        if not self._type:
            raise ValueError('Unknown type ' + type)
        
        self._orig_value = value
        self._value = value
        
        self._attrs = kwargs
        
        
        self._attrs['type'] = self._type.type_string()
        if self._type.varying():
            self._attrs['varying'] = self._type.varying()
        
        if array_count:
            self._attrs['dim'] = array_count
        
        ## If the user asked for hex, the value must be given as a hex string
        #self._value_is_hex_encoded = self._attrs.get('hex', 'off') != 'on'
        
        #if sys.version_info >= (3,0) and hasattr(value, 'decode'):
            #use_hex = true
            
            ## Value given as bytes, so we must hex encode it
            #self._value_is_hex_encoded = False
        
        #if use_hex:
            #self._hex = True
            #self._attrs['hex'] = 'on'
        #else:
            ##self._hex = False
            
            #try:
                #del self._attrs['hex']
            #except AttributeError:
                #pass
        
        #self._value = value

class DataStructure():
    def __init__(self, array_count=None, **kwargs):
        self._count = array_count
        self._attrs = kwargs
        self._fields = []
        
    def add(self, field, *args, **kwargs):
        if not isinstance(field, DataField):
            field = DataField(field, *args, **kwargs)
        
        self._fields.append(field)
        
        

class ProgramCall(_Base):
    """
    IBM i XMLSERVICE call *PGM.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iname (str): IBM i *PGM or *SRVPGM name
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'func':'MYFUNC'}       : optional - IBM i *SRVPGM function export.
        {'lib':'mylib'}         : optional - IBM i library name
        {'mode':'opm|ile'}      : optional - XMLSERVICE error choice {'mode':'ile'} 

    Example:
     iPgm('zzcall','ZZCALL')
     .addParm(iData('var1','1a','a'))
     .addParm(iData('var2','1a','b'))
     .addParm(iData('var3','7p4','32.1234'))
     .addParm(iData('var4','12p2','33.33'))
     .addParm(
      iDS('var5')
      .addData(iData('d5var1','1a','a'))
      .addData(iData('d5var2','1a','b'))
      .addData(iData('d5var3','7p4','32.1234'))
      .addData(iData('d5var4','12p2','33.33'))
      )

    Returns:
      iPgm (obj)

    Notes:
      pgm:
        <pgm name='' 
          [lib='' 
           func='' 
           mode='opm|ile' 
           error='on|off|fast'                        (1.7.6)
           ]> ... </pgm>
    """
    
    def __init__(self, name, library='*LIBL', ile=True, on_error='fast'):
        mode = 'ile' if ile else 'opm'
        super().__init__('pgm', self.__value, {'lib': library, 'name': name, 'error': on_error})
        
        self._args = OrderedDict()

    def set_args(self, **kwargs):
        for k,v in kwargs.items():
            if isinstance(v, dict):
                self.append(k, **v)
            elif isinstance(v, (DataField, DataStructure)):
                self.append(k, v)
            else:
                raise ValueError("Invalid arguments")
    
    def append(self, name, obj, type='in', by_ref=True):
        """Add a parameter child node.

        Args:
          obj   (obj): iData object or iDs object.

        Returns:
          (void)
        """
        self._args[name] = {
            'by': 'ref' if by_ref else 'val',
            'io': type,
            'value': obj,
        }
        
    def __value(self):
        """Callback to return XML value data"""
        
        data = ""
        for argname, arg in self._args:
            ""
            data += "<parm io='{}' by='{}'>{}</parm>".format(arg['io'], arg['by'], obj._xml())
        return data
    
class iToolKit:
    """
    Main iToolKit XMLSERVICE collector and output parser. 

    Args:
      include_param (num): include xml node parm output (0-no, 1-yes).
      include_return  (num): include xml node return output (0-no, 1-yes).
      inlude_ds   (num): include xml node ds output (0-no, 1-yes).
      include_row  (num): include xml node row output (0-no, 1-yes).
    
    Returns:
      iToolKit (obj)
    """
    def __init__(self, include_param=None, include_return=None, inlude_ds=1, include_row=1, transport=None):
        ## XMLSERVICE
        #self.data_keys=["cmd","pgm","sh","sql"]
        #self.data_vals=["cmd","sh","data","success","error",
                        #"xmlhint","jobipcskey","jobname","jobuser","jobnbr",
                        #"curuser","ccsid","dftccsid","paseccsid", "joblog",
                        #"jobipc","syslibl","usrlibl","version", "jobcpf"]
        #if include_param:
          #self.data_keys.append("parm")
          #self.data_vals.append("parm")
        #if include_return:
          #self.data_keys.append("return")
        #if include_row:
          #self.data_keys.append("row")
          #self.data_vals.append("row")
        #if inlude_ds:
          #self.data_keys.append("ds")

        self.transport = transport
        
        self.actions = OrderedDict()
        self._root = None
        self._xml = ""
        self.trace_fd = open(os.devnull, "a+")
        self.close_fd = True

    def clear(self):
        """Clear collecting child objects.

        Args:
          none

        Returns:
          (void)

        Notes:
          <?xml version='1.0'?>
          <xmlservice>
        """
        # XMLSERVICE
        self.actions.clear()
        self._root = None
        self._xml = ""

    def __getitem__(self, key):
        _ensure_key_is_string(key)
        
        return self.actions[key]
    
    def __setitem__(self, key, value):
        _ensure_key_is_string(key)
        if not isinstance(obj, _Base):
            raise ValueError("Object must be a _Base subclass")
        
        self.actions[key] = value
    
    def __delitem__(self, key):
        _ensure_key_is_string(key)
        
        del self.actions[key]
        
    def __contains__(self, key):
        _ensure_key_is_string(key)
        
        return key in self.actions
    
    def __iter__(self):
        return self.actions.__iter__()
    
    def __reversed__(self):
        return self.actions.__reversed__()
    
    def __len__(self):
        return len(self.actions)
    
    def keys(self):
        return self.actions.keys()
    
    def iterkeys(self):
        return self.action.iterkeys()
    
    def append(self, key_or_action, action=None):
        """Add additional child object.

        Args:
          none

        Returns:
          none

        Notes:
          <?xml version='1.0'?>
          <xmlservice>
        """
        
        # User specfied both a key and an action
        if _is_string(key_or_action) and isinstance(action, _Base):
            key = key_or_action
        # User specified just an (anonymous) action, generate a key
        elif isinstance(key_or_action, _Base) and action is None:
            key = uuid4().hex
            action = key_or_action
        elif action is None:
            raise ValueError("key_or_action must be a _Base subclass if action is None")
        elif _is_string(key_or_action):
            raise ValueError("action must be a _Base subclass if key_or_action is a string")
        else:
            raise ValueError("Unexpected error")
        
        if key in self.actions:
            raise ValueError("Key already exists")
        
        self.actions[key] = action

    def xml_in(self):
        """return raw xml input.

        Args:
          none

        Returns:
          xml
        """
        xml = "<?xml version='1.0'?>\n<xmlservice>"
        
        for key, action in self.actions.items():
          xml += action.xml_in(key)
        
        xml += "</xmlservice>\n"
        
        return xml

    def xml_out(self):
        """return raw xml output.

        Args:
          none

        Returns:
          xml
        """
        return self._xml

    def list_out(self):
        """return list output.

        Args:
          key  (num): select list from index [[0],[1],,,,].

        Returns:
          list [value]
        """
        
        return self.__parse_xml_as_list(self._root)

    def dict_out(self, key=None):
        """return dict output.

        Args:
          key  (str): select 'key' from {'key':'value'}.

        Returns:
          dict {'key':'value'}
        """
        if key is not None:
            _ensure_key_is_string(key)

        if not self._root:
            return {}
        
        output = self.__parse_xml_as_dict(self._root, 0)
        if key:
            return output[key]
        else:
            return output

    def hybrid_out(self,key=None):
        """return hybrid output.

        Args:
          key  (str): select 'key' from {'key':'value'}.

        Returns:
          hybrid {key:{'data':[list]}}
        """
        self.unq = 0
        output = {}
        _root = self._dom_out()
        self.__parse_xml_as_both(_root, output)
        if isinstance(key, str):
          try:
            return output[key]
          except KeyError:
            output[key] = {'error':output}
            return output[key]
        else:
          return output

    def enable_tracing(self, name=sys.stderr):
        """Open trace *terminal or file /tmp/python_toolkit_(name).log (1.2+)

        Args:
          name  (str): trace *terminal or file /tmp/python_toolkit_(name).log

        Returns:
          (void)
        """
        if self.trace_fd and self.close_fd:
            self.disable_tracing()
        
        path = None
        if hasattr(name, 'write'):
            self.close_fd = False
            self.trace_fd = name
        else:
            self.close_fd = True
            self.trace_fd = tempfile.TemporaryFile('a+', prefix=name, suffix='.log')
            path = self.trace_fd.name
        
        return path

    def disable_tracing(self):
        """End trace (1.2+)

        Args:
          none

        Returns:
          (void)
        """
        if self.close_fd:
            self.trace_fd.close()
        
        self.trace_fd = open(os.devnull, "a+")
        self.close_fd = True
    
    def __trace_write(self, data):
        """Write trace text (1.2+)

        Args:
          data  (str): trace text

        Returns:
          (void)
        """
        
        try:
            print(data, file=self.trace_fd)
        except Exception:
            self.disable_tracing()
            
    def __trace_write_with_time(self, data):
        self.__trace_write("{}: {}".format(time.strftime("%c"), data))

    def __trace_hexdump(self, data):
        """Write trace hexdump (1.2+)
        Args:
          data  (str): trace text
        Returns:
          (void)
        """
        
        bytes_per_line = 32
        len_max = int(math.ceil(len(data) / bytes_per_line)) * bytes_per_line
        
        for i in range(0, len_max, bytes_per_line):
            output = data[i:i+bytes_per_line]
            hex_output = binascii.hexlify(output)
            
            output = re.sub(br'[\x00-x1F]', b'.', output)
            
            self.__trace_write("<{:10}> {}".format(hex_output, output.decode('ascii')))

    def execute(self, transport=None):
        """execute xmlservice with accumulated input XML.

        Args:
          transport (obj): XMLSERVICE transport (iRestCall, iDB2Call, etc.)

        Returns:
          none
        """
        transport = transport or self.transport
        if not transport:
            raise ValueError("You must pass a transport object")
        
        xml = self.xml_in()
        
        self.__trace_write('***********************')
        self.__trace_write_with_time('control')
        self.__trace_write(transport)
        self.__trace_write_with_time('input')
        self.__trace_write(xml)
        
        def trace_exit(step):
            self.__trace_write('parse step: {} (1-OK, 2-*BADPARSE, 3-*NOPARSE)'.format(step))
            self.__parse_xml()
        
        # step 1 -- make execute
        step = 1
        try:
            xml_out = transport.execute(xml)
        except AttributeError:
            raise ValueError("Invalid transport specified")
        
        # TODO: Move this in to transport base class
        if not (xml_out and xml_out.strip()):
            xml_out = "<?xml version='1.0'?>\n<xmlservice>\n<error>*NODATA</error>\n</xmlservice>"
        
        self.__trace_write_with_time('output')
        self.__trace_write(xml_out.decode("utf-8"))
        
        self._root = fromstring(xml_out)
        trace_exit(1)
        return True
    
        try:
            self._root = fromstring(xml_out)
            trace_exit(1)
            return True
        except Exception:
            pass
        
        # step 2 -- bad parse, try modify bad output
        try:
            self.__trace_write_with_time('parse (fail)')
            self.__trace_hexdump(xml_out)
            clean1 = re.sub(r'[\x00-\x1F\x3C\x3E]', ' ', xml_out)
            clean = re.sub(' +',' ',clean1)
            xml_out = "<?xml version='1.0'?>\n<xmlservice>\n<error>*BADPARSE</error>\n<error><![CDATA["+clean+"]]></error>\n</xmlservice>"
            self._root = fromstring(xml_out)
            trace_exit(2)
            return False
        except Exception:
            pass
        
        try:
            xml_out = "<?xml version='1.0'?>\n<xmlservice>\n<error>*NOPARSE</error>\n</xmlservice>"
            self._root = fromstring(xml_out)
            trace_exit(3)
            return False
        except Exception:
            trace_exit(4)
            self._root = None
            return False
        
        
    def __parse_xml(self):
        """return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate dict{}

        Returns:
          dict {'key':'value'}
        """
        
        assert len(self._root) == 1
        assert self._root.tag == 'xmlservice'
        
        
        for child in self._root:
            key = child.attrib['var']
            self.actions[key]._parse(child)
        
        
        xml_f = BytesIO()
        ElementTree(self._root).write(xml_f, "utf-8", xml_declaration=True)
        
        self._xml = xml_f.getvalue().decode("utf-8")

    #def __include_node(self, node):
        #return node.parentNode.tag in self.data_vals and node.text != "\n"
            
    #def __parse_xml_as_list(self, parent):
        #"""return dict output.

        #Args:
          #parent (obj): parent xml.dom

        #Returns:
          #list [value]
        #"""
        #if not parent:
            #return ()
        
        #values = []
        #for child in parent.childNodes:
            #if child.nodeType == Node.TEXT_NODE or child.nodeType == Node.CDATA_SECTION_NODE:
                #if __include_node(child):
                    #values.append(child.text)
            #elif child.nodeType == Node.ELEMENT_NODE:
                #if child.tag in self.data_keys:
                    #values.append(self.__parse_xml_as_list(child))
                #else:
                    ## make sure one empty data value (1.1)
                    #if child.tag in self.data_vals and not child.childNodes:
                        #child.appendChild(self._root.createTextNode(""))
                    
                    #values.append(self.__parse_xml_as_list(child))
        
        #return tuple(values)

    #def __parse_xml_as_dict(self, parent):
        #"""return dict output.

        #Args:
          #parent (obj): parent xml.dom
          #values (obj): accumulate dict{}

        #Returns:
          #dict {'key':'value'}
        #"""
        #values = {}
        
        #if not parent:
            #return values
        
        #for child in parent.childNodes:
            #if child.nodeType == Node.TEXT_NODE or child.nodeType == Node.CDATA_SECTION_NODE:
                #if __include_node(child):
                    #var = child.parentNode.getAttribute('var')
                    #if var == "":
                        #var = child.parentNode.getAttribute('desc')
                    #if var == "":
                        #var = child.parentNode.tag
                    ## special for sql parms
                    #if child.parentNode.tag in 'parm':
                        #var = "data"
                    #myvar = var
                    #while var in values:
                        #self.unq += 1
                        #var = myvar + str(self.unq)
                    #values[var] = child.text
                    
            #elif child.nodeType == Node.ELEMENT_NODE:
                #if child.tag in self.data_keys:
                    #var = child.getAttribute('var')
                    #if var == "":
                        #var = child.tag
                    ## key was already in values
                    ## becomes list of same name
                    #child_values = {}
                    #if var in values:
                        #old = values[var]
                        #if isinstance(old,list):
                            #old.append(child_values)
                        #else:
                            #values[var] = []
                            #values[var].append(old)
                            #values[var].append(child_values)
                    #else:
                        #values[var] = child_values
                        
                    #self.__parse_xml_as_dict(child, child_values)
                #else:
                    ## make sure one empty data value (1.1)
                    #if child.tag in self.data_vals and not(child.childNodes):
                        #child.appendChild(self._root.createTextNode(""))
                    #self.__parse_xml_as_dict(child, values)

    #def __parse_xml_as_both(self, parent, values):
        #"""return dict output.

        #Args:
          #parent (obj): parent xml.dom
          #values (obj): accumulate hybrid{}

        #Returns:
          #hybrid {key:{'data':[list]}}
        #"""
        #for child in parent.childNodes:
          #if child.nodeType == Node.TEXT_NODE or child.nodeType == Node.CDATA_SECTION_NODE:
            #if __include_node(child):
              #if not 'data' in values:
                #values['data'] = []
              #values['data'].append(child.text)
          #elif child.nodeType == Node.ELEMENT_NODE:
            #if child.tag in self.data_keys:
              #var = child.getAttribute('var')
              #if var == "":
                #var = child.tag
              ## key was already in values
              ## becomes list of same name
              #child_values = {}
              #if var in values:
                #old = values[var]
                #if isinstance(old,list):
                  #old.append(child_values)
                #else:
                  #values[var] = []
                  #values[var].append(old)
                  #values[var].append(child_values)
              #else:
                #values[var] = child_values
              #self.__parse_xml_as_both(child, child_values)
            #else:
              ## make sure one empty data value (1.1)
              #if child.tag in self.data_vals and not(child.childNodes):
                #child.appendChild(self._root.createTextNode(""))
              #self.__parse_xml_as_both(child, values)



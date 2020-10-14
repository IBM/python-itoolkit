# -*- coding: utf-8 -*-
"""
IBM i python toolkit.

The toolkit runs both local and remote to IBM i using DatabaseTransport
or HttpTransport. However, class DirectTransport process local calls will
only work on IBM i (similar to IBM i CL).

Transport classes:
  class DirectTransport:      Transport XMLSERVICE direct job call
  class DatabaseTransport:    Transport XMLSERVICE calls over DB2 connection
  class HttpTransport:        Transport XMLSERVICE calls over standard HTTP

XMLSERVICE classes:
  Base:
  class iToolKit:             Main XMLSERVICE collector and output parser
  class iBase:                IBM i XMLSERVICE call addable operation(s)

  *CMDs:
  class iCmd(iBase):          IBM i XMLSERVICE call *CMD not returning *OUTPUT

  PASE:
  class iSh(iBase):           IBM i XMLSERVICE call 5250 *CMD returning *OUTPUT
  class iCmd5250(iSh):        IBM i XMLSERVICE call PASE utilities.

  *PGM or *SRVPGM:
  class iPgm (iBase):         IBM i XMLSERVICE call *PGM.
  class iSrvPgm (iPgm):       IBM i XMLSERVICE call *SRVPGM.
  class iParm (iBase):        Parameter child node for iPgm or iSrvPgm
  class iRet (iBase):         Return structure child node for iSrvPgm
  class iDS (iBase):          Data structure child node for iPgm, iSrvPgm,
                              or nested iDS data structures.
  class iData (iBase):        Data value child node for iPgm, iSrvPgm,
                              or iDS data structures.

  DB2:
  class iSqlQuery (iBase):    IBM i XMLSERVICE direct execute SQL statement
  class iSqlPrepare (iBase):  IBM i XMLSERVICE prepare SQL statement
  class iSqlExecute (iBase):  IBM i XMLSERVICE execute a prepared statement
  class iSqlFetch (iBase):    IBM i XMLSERVICE fetch rows of statement
  class iSqlParm (iBase):     Parameter child node for iSqlExecute
  class iSqlFree (iBase):     IBM i XMLSERVICE free open handles

  Anything (XMLSERVICE XML, if no class exists):
  class iXml(iBase):          IBM i XMLSERVICE raw xml input

Import:
  1) XMLSERVICE direct call (current job) - local only
  from itoolkit import *
  from itoolkit.transport import DirectTransport
  itransport = DirectTransport()

  2) XMLSERVICE db2 call (QSQSRVR job) - local/remote
  from itoolkit import *
  from itoolkit.transport import DatabaseTransport
  conn = ibm_db_dbi.connect()
  itransport = DatabaseTransport(conn)

  3) XMLSERVICE http/rest/web call (Apache job) - local/remote
  from itoolkit import *
  from itoolkit.transport import HttpTransport
  itransport = HttpTransport(url,user,password)

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
import xml.dom.minidom
import re
import time

try:
    from shlex import quote
except ImportError:
    # python2 has shlex, but not shlex.quote
    # Implement a crude equivalent. We don't care about Python 2 that much
    def quote(s):
        if ' ' not in s:
            return s

        # remove first and last space to be less confusing
        quote_replacement = """ '"'"' """[1:-1]
        return "'" + s.replace("'", quote_replacement) + "'"

class iBase(object): # noqa N801
    """
    IBM i XMLSERVICE call addable operation(s).

      Args:
        iopt (dict): user options (see descendents)
        idft (dict): default options (see descendents)

      Example:
        itransport = DirectTransport()
        itool = iToolKit()
        itool.add(iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE)'))
        itool.add(iSh('ps', 'ps -ef'))
        ... so on ...
        itool.call(itransport)

      Returns:
        iBase (obj)

      Notes:
        iopt  (dict): XMLSERVICE elements, attributes and values
                      'k' - element <x>
                      'v' - value <x>value</x>
                      'i' - attribute <x var='ikey'>
                      'c' - iBase children
                      ... many more idft + iopt ...
                      'error' - <x 'error'='fast'>
    """

    def __init__(self, iopt={}, idft={}):
        # xml defaults
        self.opt = idft.copy()
        self.opt.update(iopt)

        # my children objects
        self.opt['c'] = []

    def add(self, obj):
        """Additional mini dom xml child nodes.

        Args:
          obj (iBase) : additional child object

        Example:
          itool = iToolKit()
          itool.add(
            iPgm('zzcall','ZZCALL')             <--- child of iToolkit
            .addParm(iData('INCHARA','1a','a')) <--- child of iPgm
            )

        Returns:
          (void)
        """
        self.opt['c'].append(obj)

    def xml_in(self):
        """Return XML string of collected mini dom xml child nodes.

        Args:
          none

        Returns:
          XML (str)
        """
        return self.make().toxml()

    def make(self):
        """Assemble coherent mini dom xml, including child nodes.

        Args:
          none

        Returns:
          xml.dom.minidom (obj)
        """
        # XMLSERVICE
        xmli = ""
        if 'j' in self.opt:
            xmli += '<' + self.opt['j'] + " var='" + self.opt['i'] + "'>\n"
        xmli += '<' + self.opt['k']
        for k, v in self.opt.items():
            if len(k) > 1:
                xmli += " " + k + "='" + str(v) + "'"
        xmli += " var='" + self.opt['i'] + "'>"
        if len(self.opt['v']) > 0:
            xmli += '<![CDATA[' + self.opt['v'] + ']]>'
        xmli += '</' + self.opt['k'] + '>' + "\n"
        if 'j' in self.opt:
            xmli += '</' + self.opt['j'] + '>' + "\n"
        # build my children
        parent = xml.dom.minidom.parseString(xmli).firstChild
        for obj in self.opt['c']:
            if parent.tagName == "sql" and isinstance(obj, iSqlParm):
                parent.childNodes[1].appendChild(obj.make())
            else:
                parent.appendChild(obj.make())
        return parent


class iCmd(iBase): # noqa N801
    """
    IBM i XMLSERVICE call *CMD not returning *OUTPUT.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i command no output (see 5250 command prompt).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'}   : XMLSERVICE error option
        {'exec':cmd|system|rexx'} : XMLSERVICE command type {'exec':'cmd'}
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

    def __init__(self, ikey, icmd, iopt={}):
        opts = {
            'i': ikey,
            'k': 'cmd',
            'v': icmd,
            'exec': 'rexx' if '?' in icmd else 'cmd',
            'error': 'fast'
        }
        super(iCmd, self).__init__(iopt, opts)


class iSh(iBase): # noqa N801
    """
    IBM i XMLSERVICE call PASE utilities.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i PASE script/utility (see call qp2term).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'row':'on|off'}        : XMLSERVICE wrap line in row tag? {'row':'off'}

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

    def __init__(self, ikey, icmd, iopt={}):
        opts = {
            'i': ikey,
            'k': 'sh',
            'v': icmd,
            'error': 'fast'
        }
        super(iSh, self).__init__(iopt, opts)


class iCmd5250(iSh): # noqa N801
    """
    IBM i XMLSERVICE call 5250 *CMD returning *OUTPUT.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i PASE script/utility (see call qp2term).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'row':'on|off'}        : XMLSERVICE wrap line in row tag? {'row':'off'}

    Example:
      iCmd5250('dsplibl','dsplibl')
      iCmd5250('wrkactjob','wrkactjob')

    Returns:
      iCmd5250 (obj)

    Notes:
      This is a subclass of iSh, therefore XMLSERVICE perfoms
      standard PASE shell popen fork/exec calls.

      /QOpenSys/usr/bin/system 'wrkactjob'

      Please note, this is a relatively slow operation,
      use sparingly on high volume web sites.

      <sh [rows='on|off'
           hex='on' before='cc1/cc2/cc3/cc4' after='cc4/cc3/cc2/cc1' (1.7.4)
           error='on|off|fast'                                       (1.7.6)
           ]>(PASE utility)</sh>
    """

    def __init__(self, ikey, icmd, iopt={}):
        cmd = "/QOpenSys/usr/bin/system " + quote(icmd)
        super(iCmd5250, self).__init__(ikey, cmd, iopt)


class iPgm (iBase): # noqa N801
    """
    IBM i XMLSERVICE call *PGM.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iname (str): IBM i *PGM or *SRVPGM name
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'func':'MYFUNC'}       : IBM i *SRVPGM function export.
        {'lib':'mylib'}         : IBM i library name
        {'mode':'opm|ile'}      : XMLSERVICE error choice {'mode':'ile'}

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

    def __init__(self, ikey, iname, iopt={}):
        opts = {
            'i': ikey,
            'k': 'pgm',
            'v': '',
            'name': iname,
            'error': 'fast'
        }
        super(iPgm, self).__init__(iopt, opts)
        self.pcnt = 0

    def addParm(self, obj, iopt={}): # noqa N802
        """Add a parameter child node.

        Args:
          obj   (obj): iData object or iDs object.
          iopt (dict): options to pass to iParm constructor

        Returns:
          (void)
        """
        self.pcnt += 1
        p = iParm('p' + str(self.pcnt), iopt)
        p.add(obj)
        self.add(p)
        return self


class iSrvPgm (iPgm): # noqa N801
    """
    IBM i XMLSERVICE call *SRVPGM.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iname (str): IBM i *PGM or *SRVPGM name
      ifunc (str): IBM i *SRVPGM function export.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'lib':'mylib'}         : IBM i library name
        {'mode':'opm|ile'}      : XMLSERVICE error choice {'mode':'ile'}

    Example:
      see iPgm

    Returns:
      iSrvPgm (obj)

    Notes:
      pgm:
        <pgm name=''
          [lib=''
           func=''
           mode='opm|ile'
           error='on|off|fast'                        (1.7.6)
           ]> ... </pgm>
    """

    def __init__(self, ikey, iname, ifunc, iopt={}):
        iopt = iopt.copy()
        iopt['func'] = ifunc
        super(iSrvPgm, self).__init__(ikey, iname, iopt)

    def addRet(self, obj): # noqa N802
        """Add a return structure child node.

        Args:
          obj   (obj): iData object or iDs object.

        Returns:
          (void)
        """
        self.pcnt += 1
        p = iRet('r' + str(self.pcnt))
        p.add(obj)
        self.add(p)
        return self


class iParm (iBase): # noqa N801
    """
    Parameter child node for iPgm or iSrvPgm (see iPgm.addParm)

    Args:
      ikey  (str): ikey  (str): XML <parm ... var="ikey"> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'io':'in|out|both|omit'} : XMLSERVICE param type {'io':both'}.

    Example:
      see iPgm

    Returns:
      iParm (obj)

    Notes:
      This class is not used directly, but is used by iPgm.addParm
      or iSrvPgm.addParm.

      pgm parameters:
        <pgm>
        <parm [io='in|out|both|omit'                  (omit 1.2.3)
               by='val|ref'
               ]>(see <ds> and <data>)</parm>
        </pgm>
    """

    def __init__(self, ikey, iopt={}):
        opts = {
            'i': ikey,
            'k': 'parm',
            'v': '',
            'io': 'both'
        }
        super(iParm, self).__init__(iopt, opts)


class iRet (iBase): # noqa N801
    """
    Return structure child node for iSrvPgm (see iSrvPgm.addRet)

    Args:
      ikey  (str): XML <return ... var="ikey"> for parsing output.

    Example:
      see iPgm

    Returns:
      iRet (obj)

    Notes:
      This class is not used directly, but is used by iSrvPgm.addRet.

      pgm return:
        <pgm>
        <return>(see <ds> and <data>)</return>
        </pgm>
    """

    def __init__(self, ikey):
        opts = {
            'i': ikey,
            'k': 'return',
            'v': ''
        }
        super(iRet, self).__init__({}, opts)


class iDS (iBase): # noqa N801
    """
    Data structure child node for iPgm, iSrvPgm,
    or nested iDS data structures.

    Args:
      ikey  (str): XML <ds ... var="ikey"> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'dim':'n'}     : XMLSERVICE dimension/occurs number.
        {'dou':'label'} : XMLSERVICE do until label.
        {'len':'label'} : XMLSERVICE calc length label.

    Example:
      see iPgm

    Returns:
      iDS (obj)

    Notes:
      pgm data structure:
        <ds [dim='n' dou='label'
             len='label'                                 (1.5.4)
             data='records'                              (1.7.5)
             ]>(see <data>)</ds>
    """

    def __init__(self, ikey, iopt={}):
        opts = {
            'i': ikey,
            'k': 'ds',
            'v': ''
        }
        super(iDS, self).__init__(iopt, opts)

    def addData(self, obj): # noqa N802
        """Add a iData or iDS child node.

        Args:
          obj   (obj): iData object or iDs object.

        Returns:
          (void)
        """
        self.add(obj)
        return self


class iData (iBase): # noqa N801
    """
    Data value child node for iPgm, iSrvPgm,
    or iDS data structures.

    Args:
      ikey  (str): XML <data ... var="ikey"> for parsing output.
      iparm (obj): dom for parameter or return or ds.
      itype (obj): data type [see XMLSERVICE types, '3i0', ...].
      ival  (obj): data type value.
      iopt (dict): option - dictionay of options (below)
        {'dim':'n'}               : XMLSERVICE dimension/occurs number.
        {'varying':'on|off|2|4'}  : XMLSERVICE varying {'varying':'off'}.
        {'hex':'on|off'}          : XMLSERVICE hex chracter data {'hex':'off'}.
        {'enddo':'label'}         : XMLSERVICE enddo until label.
        {'setlen':'label'}        : XMLSERVICE set calc length label.
        {'offset':'n'}            : XMLSERVICE offset label.
        {'next':'label'}          : XMLSERVICE next offset label (value).

    Example:
      see iPgm

    Returns:
      iData (obj)

    Notes:
      pgm data elements:
        <data type='data types'
           [dim='n'
            varying='on|off|2|4'
            enddo='label'
            setlen='label'             (1.5.4)
            offset='label'
            hex='on|off'               (1.6.8)
            before='cc1/cc2/cc3/cc4'   (1.6.8)
            after='cc4/cc3/cc2/cc1'    (1.6.8)
            trim='on|off'              (1.7.1)
            next='nextoff'             (1.9.2)
            ]>(value)</data>

        For more info on data types you can use, refer to
        http://yips.idevcloud.com/wiki/index.php/XMLService/DataTypes

    .. versionchanged:: 1.6.3
        `ival` is now optional and supports non-string parameters.
    """

    def __init__(self, ikey, itype, ival="", iopt={}):
        opts = {
            'i': ikey,
            'k': 'data',
            'v': str(ival) if ival is not None else "",
            'type': itype
        }
        super(iData, self).__init__(iopt, opts)


class iSqlQuery (iBase): # noqa N801
    """
    IBM i XMLSERVICE call DB2 execute direct SQL statement.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      isql  (str): IBM i query (see 5250 strsql).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'conn':'label'}        : XMLSERVICE connection label
        {'stmt':'label'}        : XMLSERVICE stmt label
        {'options':'label'}     : XMLSERVICE options label

    Example:
      iSqlQuery('custquery', "select * from QIWS.QCUSTCDT where LSTNAM='Jones'")
      iSqlFetch('custfetch')

    Returns:
      iSqlQuery (obj)
    """

    def __init__(self, ikey, isql, iopt={}):
        opts = {
            'i': ikey,
            'j': 'sql',
            'k': 'query',
            'v': isql,
            'error': 'fast'
        }
        super(iSqlQuery, self).__init__(iopt, opts)


class iSqlPrepare (iBase): # noqa N801
    """
    IBM i XMLSERVICE call DB2 prepare SQL statement.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      isql  (str): IBM i query (see 5250 strsql).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'conn':'label'}        : XMLSERVICE connection label
        {'stmt':'label'}        : XMLSERVICE stmt label
        {'options':'label'}     : XMLSERVICE options label

    Example:
      iSqlPrepare('callprep', "call mylib/mycall(?,?,?)")
      iSqlExecute('callexec')
       .addParm(iSqlParm('var1','a'))
       .addParm(iSqlParm('var2','b'))
       .addParm(iSqlParm('var3','32.1234'))
      iSqlFetch('callfetch')
      iSqlFree('alldone')

    Returns:
      iSqlPrepare (obj)
    """

    def __init__(self, ikey, isql, iopt={}):
        opts = {
            'i': ikey,
            'j': 'sql',
            'k': 'prepare',
            'v': isql,
            'error': 'fast'
        }
        super(iSqlPrepare, self).__init__(iopt, opts)


class iSqlExecute (iBase): # noqa N801
    """
    IBM i XMLSERVICE call execute a DB2 prepare SQL statement.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'conn':'label'}        : XMLSERVICE connection label
        {'stmt':'label'}        : XMLSERVICE stmt label
        {'options':'label'}     : XMLSERVICE options label

    Example:
      see iSqlPrepare

    Returns:
      iSqlExecute (obj)

    Notes:
      <sql><execute [stmt='label'  error='on|off|fast']></sql>
    """

    def __init__(self, ikey, iopt={}):
        opts = {
            'i': ikey,
            'j': 'sql',
            'k': 'execute',
            'v': '',
            'error': 'fast'
        }
        super(iSqlExecute, self).__init__(iopt, opts)
        self.pcnt = 0

    def addParm(self, obj): # noqa N802
        """Add a iSqlParm child node.

        Args:
          obj   (obj): iSqlParm object.

        Returns:
          (void)
        """
        self.add(obj)
        return self


class iSqlFetch (iBase): # noqa N801
    """
    IBM i XMLSERVICE call DB2 fetch results/rows of SQL statement.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'stmt':'label'}        : XMLSERVICE stmt label
        {'block':'all|n'}       : XMLSERVICE block records {'block':'all'}
        {'desc':'on|off'}       : XMLSERVICE block records {'desc':'on'}
        {'rec':'n'}             : XMLSERVICE block records

    Example:
      see iSqlPrepare or iSqlQuery

    Returns:
      none
    """

    def __init__(self, ikey, iopt={}):
        opts = {
            'i': ikey,
            'j': 'sql',
            'k': 'fetch',
            'v': '',
            'block': 'all',
            'error': 'fast'
        }
        super(iSqlFetch, self).__init__(iopt, opts)


class iSqlParm (iBase): # noqa N801
    """
    Parameter child node for iSqlExecute (see iSqlExecute.addParm)

    Args:
      ikey  (str): XML <parm ... var="ikey"> for parsing output.
      ival  (str): data value.
      iopt (dict): option - dictionay of options (below)
        {'io':'in|out|both|omit'} : XMLSERVICE param type {'io':both'}.

    Example:
      see iSqlPrepare

    Returns:
      iSqlParm (obj)

    Notes:
      This class is not used directly, but is used by iSqlExecute.addParm.

      <sql>
      <execute>
      <parm [io='in|out|both']>val</parm>
      </execute>
      <sql>
    """

    def __init__(self, ikey, ival, iopt={}):
        opts = {
            'i': ikey,
            'k': 'parm',
            'v': ival,
            'io': 'both'
        }
        super(iSqlParm, self).__init__(iopt, opts)


class iSqlFree (iBase): # noqa N801
    """
    IBM i XMLSERVICE call DB2 free open handles.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice
        {'conn':'all|label'}    : XMLSERVICE free connection label
        {'cstmt':'label'}       : XMLSERVICE free connection label statements
        {'stmt':'all|label'}    : XMLSERVICE free stmt label
        {'options':'all|label'} : XMLSERVICE free options label

    Example:
      see iSqlPrepare

    Returns:
      iSqlFree (obj)

    Notes:
      <sql>
      <free [conn='all|label'
        cstmt='label'
        stmt='all|label'
        options='all|label'
        error='on|off|fast']/>
      </sql>
    """

    def __init__(self, ikey, iopt={}):
        opts = {
            'i': ikey,
            'j': 'sql',
            'k': 'free',
            'v': '',
            'error': 'fast'
        }
        super(iSqlFree, self).__init__(iopt, opts)


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
        super(iXml, self).__init__()
        self.xml_body = ixml

    def add(self, obj):
        """add input not allowed.

        Returns:
          raise except
        """
        raise

    def make(self):
        """Assemble coherent mini dom xml.

        Args:
          none

        Returns:
          xml.dom.minidom (obj)
        """
        try:
            dom = xml.dom.minidom.parseString(self.xml_body).firstChild
        except xml.parsers.expat.ExpatError as e:
            e.args += (self.xml_body,)
            raise
        return dom


class iToolKit(object): # noqa N801
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
        self.trace_fd = False

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
        self.input = []
        self.domo = ""

    def add(self, obj):
        """Add additional child object.

        Args:
          none

        Returns:
          none

        Notes:
          <?xml version='1.0'?>
          <xmlservice>
        """
        self.input.append(obj)

    def xml_in(self):
        """return raw xml input.

        Args:
          none

        Returns:
          xml
        """
        xmli = "<?xml version='1.0'?>\n<xmlservice>"
        for v in self.input:
            xmli += v.xml_in()
        xmli += "</xmlservice>\n"
        return xmli

    def xml_out(self):
        """return raw xml output.

        Args:
          none

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
        """Open trace *terminal or file /tmp/python_toolkit_(iname).log (1.2+)

        Args:
          iname  (str): trace *terminal or file /tmp/python_toolkit_(iname).log

        Returns:
          (void)
        """
        if self.trace_fd:
            self.trace_close()
        if '*' in iname:
            self.trace_fd = iname
        else:
            self.trace_fd = open('/tmp/python_toolkit_' + iname + '.log', 'a+')

    def trace_write(self, itext):
        """Write trace text (1.2+)

        Args:
          itext  (str): trace text

        Returns:
          (void)
        """
        if self.trace_fd:
            try:
                if '*' in str(self.trace_fd):
                    print(itext)
                else:
                    self.trace_fd.write(itext + '\n')
            except Exception:
                self.trace_close()

    def trace_hexdump(self, itext):
        """Write trace hexdump (1.2+)
        Args:
          itext  (str): trace text
        Returns:
          (void)
        """
        if self.trace_fd:
            result = ''
            text = ''
            for c in itext:
                result += "%02x" % ord(c)
                text += re.sub(r'[\x00-\x1F]', '.', c)
                if len(result) >= 32:
                    self.trace_write(result + " " + text)
                    result = ''
                    text = ''
            if len(result):
                self.trace_write(result + " " + text)

    def trace_close(self):
        """End trace (1.2+)

        Args:
          none

        Returns:
          (void)
        """
        if self.trace_fd:
            if '*' not in str(self.trace_fd):
                self.trace_fd.close()
        self.trace_fd = False

    def call(self, itrans):
        """Call xmlservice with accumulated input XML.

        Args:
          itrans (obj): XMLSERVICE transport object

        Returns:
          none

        Raises:
          TransportClosedException: If the transport has been closed.
        """
        if self.trace_fd:
            self.trace_write('***********************')
            self.trace_write('control ' + time.strftime("%c"))
            self.trace_write(itrans.trace_data())
            self.trace_write('input ' + time.strftime("%c"))
            self.trace_write(self.xml_in())
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
            if self.trace_fd:
                self.trace_write('output ' + time.strftime("%c"))
                self.trace_write(xml_out)
            domo = xml.dom.minidom.parseString(xml_out)
        except Exception:
            step = 2
        # step 2 -- bad parse, try modify bad output
        if step == 2:
            try:
                if self.trace_fd:
                    self.trace_write('parse (fail) ' + time.strftime("%c"))
                    self.trace_hexdump(xml_out)
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
        if self.trace_fd:
            self.trace_write(
                'parse step: ' +
                str(step) +
                ' (1-ok, 2-*BADPARSE, 3-*NOPARSE)')
        self.domo = domo

    def _dom_out(self):
        """return xmlservice dom output.

        Args:
          none

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

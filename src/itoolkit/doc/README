


IBM i python toolkit. 

The toolkit runs both local and remote to IBM i using iDB2Call or iRestCall. 
However, class iLibCall process local calls will only work on IBM i (similar to IBM i CL).

Transport classes:
  class iLibCall:             Transport XMLSERVICE direct job call (within job/process calls).
  class iDB2Call:             Transport XMLSERVICE calls over DB2 connection.
  class iRestCall:            Transport XMLSERVICE calls over standard HTTP rest.

XMLSERVICE classes:
  Base:
  class iToolKit:             Main iToolKit XMLSERVICE collector and output parser.
  class iBase:                IBM i XMLSERVICE call addable operation(s).

  *CMDs:
  class iCmd(iBase):          IBM i XMLSERVICE call *CMD not returning *OUTPUT.

  PASE:
  class iSh(iBase):           IBM i XMLSERVICE call 5250 *CMD returning *OUTPUT.
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
  class iSqlQuery (iBase):    IBM i XMLSERVICE call DB2 execute direct SQL statment.
  class iSqlPrepare (iBase):  IBM i XMLSERVICE call DB2 prepare SQL statment.
  class iSqlExecute (iBase):  IBM i XMLSERVICE call execute a DB2 prepare SQL statment.
  class iSqlFetch (iBase):    IBM i XMLSERVICE call DB2 fetch results/rows of SQL statment.
  class iSqlParm (iBase):     Parameter child node for iSqlExecute.
  class iSqlFree (iBase):     IBM i XMLSERVICE call DB2 free open handles.

  Anything (XMLSERVICE XML, if no class exists):
  class iXml(iBase):          IBM i XMLSERVICE raw xml input.

Import:
  1) XMLSERVICE direct call (current job) - local only
  from itoolkit import *
  from itoolkit.lib.ilibcall import *
  itransport = iLibCall()

  2) XMLSERVICE db2 call (QSQSRVR job) - local/remote
  from itoolkit import *
  from itoolkit.db2.idb2call import *
  itransport = iDB2Call(user,password)
  -- or -
  conn = ibm_db.connect(database, user, password)
  itransport = iDB2Call(conn)

  3) XMLSERVICE http/rest/web call (Apache job) - local/remote
  from itoolkit import *
  from itoolkit.rest.irestcall import *
  itransport = iRestCall(url,user,password)

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



class iBase:
    
    IBM i XMLSERVICE call addable operation(s).

      Args:
        iopt (dict): user options (see descendents)
        idft (dict): default options (see descendents)

      Example:
        itransport = iLibCall()
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


    def __init__(self, iopt={}, idft={}):


    def add(self, obj):
        Additional mini dom xml child nodes.

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


    def xml_in(self):
        Return XML string of collected mini dom xml child nodes.

        Args:
          none

        Returns:
          XML (str)


    def make(self):
        Assemble coherent mini dom xml, including child nodes.

        Args:
          none

        Returns:
          xml.dom.minidom (obj)


class iCmd(iBase):
    
    IBM i XMLSERVICE call *CMD not returning *OUTPUT.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
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


    def __init__(self, ikey, icmd, iopt={}):


class iSh(iBase):
    
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


    def __init__(self, ikey, icmd, iopt={}):


class iCmd5250(iSh):
    
    IBM i XMLSERVICE call 5250 *CMD returning *OUTPUT.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i PASE script/utility (see call qp2term).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'}  : optional - XMLSERVICE error choice {'error':'fast'}
        {'row':'on|off'}         : optional - XMLSERVICE <row>line output</row> choice {'row':'off'}

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


    def __init__(self, ikey, icmd, iopt={}):


class iPgm (iBase):
    
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


    def __init__(self, ikey, iname, iopt={}):


    def addParm(self, obj):
        Add a parameter child node.

        Args:
          obj   (obj): iData object or iDs object.

        Returns:
          (void)


class iSrvPgm (iPgm):
    
    IBM i XMLSERVICE call *SRVPGM.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iname (str): IBM i *PGM or *SRVPGM name
      ifunc (str): IBM i *SRVPGM function export.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'lib':'mylib'}         : optional - IBM i library name
        {'mode':'opm|ile'}      : optional - XMLSERVICE error choice {'mode':'ile'} 

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


    def __init__(self, ikey, iname, ifunc, iopt={}):


    def addRet(self, obj):
        Add a return structure child node.

        Args:
          obj   (obj): iData object or iDs object.

        Returns:
          (void)


class iParm (iBase):
    
    Parameter child node for iPgm or iSrvPgm (see iPgm.addParm)

    Args:
      ikey  (str): ikey  (str): XML <parm ... var="ikey"> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'io':'in|out|both|omit'} : optional - XMLSERVICE param type {'io':both'}.

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


    def __init__(self, ikey, iopt={}):


class iRet (iBase):
    
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


    def __init__(self, ikey):


class iDS (iBase):
    
    Data structure child node for iPgm, iSrvPgm,
    or nested iDS data structures.

    Args:
      ikey  (str): XML <ds ... var="ikey"> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'dim':'n'}     : optional - XMLSERVICE dimension/occurs number.
        {'dou':'label'} : optional - XMLSERVICE do until label.
        {'len':'label'} : optional - XMLSERVICE calc length label.

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


    def __init__(self, ikey, iopt={}):


    def addData(self, obj):
        Add a iData or iDS child node.

        Args:
          obj   (obj): iData object or iDs object.

        Returns:
          (void)


class iData (iBase):
    
    Data value child node for iPgm, iSrvPgm,
    or iDS data structures.

    Args:
      ikey  (str): XML <data ... var="ikey"> for parsing output.
      iparm (obj): dom for parameter or return or ds.
      itype (obj): data type [see XMLSERVICE types, '3i0', ...].
      ival  (obj): data type value.
      iopt (dict): option - dictionay of options (below)
        {'dim':'n'}               : optional - XMLSERVICE dimension/occurs number.
        {'varying':'on|off|2|4'}  : optional - XMLSERVICE varying {'varying':'off'}.
        {'hex':'on|off'}          : optional - XMLSERVICE hex chracter data {'hex':'off'}.
        {'enddo':'label'}         : optional - XMLSERVICE enddo until label.
        {'setlen':'label'}        : optional - XMLSERVICE set calc length label.
        {'offset':'n'}            : optional - XMLSERVICE offset label.
        {'next':'label'}          : optional - XMLSERVICE next offset label (value).

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
            setlen='label'                                                (1.5.4)
            offset='label'
            hex='on|off' before='cc1/cc2/cc3/cc4' after='cc4/cc3/cc2/cc1' (1.6.8)
            trim='on|off'                                                 (1.7.1)
            next='nextoff'                                                (1.9.2)
            ]>(value)</data>

      C types          RPG types                     XMLSERVICE types                                   SQL types
      ===============  ============================  ================================================   =========
      int8/byte        D myint8    3i 0              <data type='3i0'/>                                 TINYINT   (unsupported DB2)
      int16/short      D myint16   5i 0 (4b 0)       <data type='5i0'/>                                 SMALLINT
      int32/int        D myint32  10i 0 (9b 0)       <data type='10i0'/>                                INTEGER
      int64/longlong   D myint64  20i 0              <data type='20i0'/>                                BIGINT
      uint8/ubyte      D myuint8   3u 0              <data type='3u0'/>
      uint16/ushort    D myuint16  5u 0              <data type='5u0'/>
      uint32/uint      D myuint32 10u 0              <data type='10u0'/>
      uint64/ulonglong D myuint64 20u 0              <data type='20u0'/>
      char             D mychar   32a                <data type='32a'/>                                 CHAR(32)
      varchar2         D myvchar2 32a   varying      <data type='32a' varying='on'/>                    VARCHAR(32)
      varchar4         D myvchar4 32a   varying(4)   <data type='32a' varying='4'/>
      packed           D mydec    12p 2              <data type='12p2'/>                                DECIMAL(12,2)
      zoned            D myzone   12s 2              <data type='12s2'/>                                NUMERIC(12,2)
      float            D myfloat   4f                <data type='4f2'/>                                 FLOAT
      real/double      D myreal    8f                <data type='8f4'/>                                 REAL
      binary           D mybin    (any)              <data type='9b'>F1F2F3</data>                      BINARY
      hole (no out)    D myhole   (any)              <data type='40h'/>
      boolean          D mybool    1n                <data type='4a'/>                                  CHAR(4)
      time             D mytime     T   timfmt(*iso) <data type='8A'>09.45.29</data>                    TIME
      timestamp        D mystamp    Z                <data type='26A'>2011-12-29-12.45.29.000000</data> TIMESTAMP
      date             D mydate     D   datfmt(*iso) <data type='10A'>2009-05-11</data>                 DATE


    def __init__(self, ikey, itype, ival, iopt={}):


class iSqlQuery (iBase):
    
    IBM i XMLSERVICE call DB2 execute direct SQL statment.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      isql  (str): IBM i query (see 5250 strsql).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'conn':'label'}        : optional - XMLSERVICE connection label
        {'stmt':'label'}        : optional - XMLSERVICE stmt label
        {'options':'label'}     : optional - XMLSERVICE options label

    Example:
      iSqlQuery('custquery', "select * from QIWS.QCUSTCDT where LSTNAM='Jones' or LSTNAM='Vine'")
      iSqlFetch('custfetch')

    Returns:
      iSqlQuery (obj)

    Notes:
      <sql><query [conn='label' stmt='label' options='label' error='on|off|fast']></sql>


    def __init__(self, ikey, isql, iopt={}):


class iSqlPrepare (iBase):
    
    IBM i XMLSERVICE call DB2 prepare SQL statment.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      isql  (str): IBM i query (see 5250 strsql).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'conn':'label'}        : optional - XMLSERVICE connection label
        {'stmt':'label'}        : optional - XMLSERVICE stmt label
        {'options':'label'}     : optional - XMLSERVICE options label

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

    Notes:
      <sql><prepare [conn='label' stmt='label' options='label' error='on|off|fast']></sql>


    def __init__(self, ikey, isql, iopt={}):


class iSqlExecute (iBase):
    
    IBM i XMLSERVICE call execute a DB2 prepare SQL statment.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'conn':'label'}        : optional - XMLSERVICE connection label
        {'stmt':'label'}        : optional - XMLSERVICE stmt label
        {'options':'label'}     : optional - XMLSERVICE options label

    Example:
      see iSqlPrepare

    Returns:
      iSqlExecute (obj)

    Notes:
      <sql><execute [stmt='label'  error='on|off|fast']></sql>


    def __init__(self, ikey, iopt={}):


    def addParm(self, obj):
        Add a iSqlParm child node.

        Args:
          obj   (obj): iSqlParm object.

        Returns:
          (void)


class iSqlFetch (iBase):
    
    IBM i XMLSERVICE call DB2 fetch results/rows of SQL statment.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'stmt':'label'}        : optional - XMLSERVICE stmt label
        {'block':'all|n'}       : optional - XMLSERVICE block records {'block':'all'}
        {'desc':'on|off'}       : optional - XMLSERVICE block records {'desc':'on'}
        {'rec':'n'}             : optional - XMLSERVICE block records

    Example:
      see iSqlPrepare or iSqlQuery

    Returns:
      none

    Notes:
      <sql>
      <fetch [stmt='label' block='all|n' rec='n' desc='on|off' error="on|off|fast"/>
                          (default=all)         (default=on)  (default='off')
      </sql>


    def __init__(self, ikey, iopt={}):


class iSqlParm (iBase):
    
    Parameter child node for iSqlExecute (see iSqlExecute.addParm)

    Args:
      ikey  (str): XML <parm ... var="ikey"> for parsing output.
      ival  (str): data value.
      iopt (dict): option - dictionay of options (below)
        {'io':'in|out|both|omit'} : optional - XMLSERVICE param type {'io':both'}.

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


    def __init__(self, ikey, ival, iopt={}):


class iSqlFree (iBase):
    
    IBM i XMLSERVICE call DB2 free open handles.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : optional - XMLSERVICE error choice {'error':'fast'}
        {'conn':'all|label'}    : optional - XMLSERVICE free connection label
        {'cstmt':'label'}       : optional - XMLSERVICE free connection label statements
        {'stmt':'all|label'}    : optional - XMLSERVICE free stmt label
        {'options':'all|label'} : optional - XMLSERVICE free options label

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


    def __init__(self, ikey, iopt={}):


class iXml(iBase):
    
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


    def __init__(self, ixml):


    def add(self, obj):
        add input not allowed.

        Returns:
          raise except


    def make(self):
        Assemble coherent mini dom xml.

        Args:
          none

        Returns:
          xml.dom.minidom (obj)


class iToolKit:
    
    Main iToolKit XMLSERVICE collector and output parser. 

    Args:
      iparm (num): include xml node parm output (0-no, 1-yes).
      iret  (num): include xml node return output (0-no, 1-yes).
      ids   (num): include xml node ds output (0-no, 1-yes).
      irow  (num): include xml node row output (0-no, 1-yes).
    
    Returns:
      iToolKit (obj)


    def __init__(self, iparm=0, iret=0, ids=1, irow=1):


    def clear(self):
        Clear collecting child objects.

        Args:
          none

        Returns:
          (void)

        Notes:
          <?xml version='1.0'?>
          <xmlservice>


    def add(self, obj):
        Add additional child object.

        Args:
          none

        Returns:
          none

        Notes:
          <?xml version='1.0'?>
          <xmlservice>


    def xml_in(self):
        return raw xml input.

        Args:
          none

        Returns:
          xml


    def xml_out(self):
        return raw xml output.

        Args:
          none

        Returns:
          xml


    def list_out(self,ikey=-1):
        return list output.

        Args:
          ikey  (num): select list from index [[0],[1],,,,].

        Returns:
          list [value]


    def dict_out(self,ikey=0):
        return dict output.

        Args:
          ikey  (str): select 'key' from {'key':'value'}.

        Returns:
          dict {'key':'value'}


    def hybrid_out(self,ikey=0):
        return hybrid output.

        Args:
          ikey  (str): select 'key' from {'key':'value'}.

        Returns:
          hybrid {key:{'data':[list]}}


    def trace_open(self,iname='*terminal'):
        Open trace *terminal or file /tmp/python_toolkit_(iname).log (1.2+)

        Args:
          iname  (str): trace *terminal or file /tmp/python_toolkit_(iname).log

        Returns:
          (void)


    def trace_write(self,itext):
        Write trace text (1.2+)

        Args:
          itext  (str): trace text

        Returns:
          (void)


    def trace_hexdump(self,itext):
        Write trace hexdump (1.2+)
        Args:
          itext  (str): trace text
        Returns:
          (void)


    def trace_close(self):
        End trace (1.2+)

        Args:
          none

        Returns:
          (void)


    def call(self, itrans):
        Call xmlservice with accumulated input XML.

        Args:
          itrans (obj): XMLSERVICE transport (iRestCall, iDB2Call, etc.)

        Returns:
          none


    def _dom_out(self):
        return xmlservice dom output.

        Args:
          none

        Returns:
          xml.dom


    def _parseXmlList(self, parent, values):
        return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate list []

        Returns:
          list [value]


    def _parseXmlDict(self, parent, values):
        return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate dict{}

        Returns:
          dict {'key':'value'}


    def _parseXmlHybrid(self, parent, values):
        return dict output.

        Args:
          parent (obj): parent xml.dom
          values (obj): accumulate hybrid{}

        Returns:
          hybrid {key:{'data':[list]}}




class iDB2Call:
    
    Transport XMLSERVICE calls over DB2 connection.

    Args:
      iuid   (str): Database user profile name or database connection
      ipwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass) 
      idb2   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      isiz   (int): optional - XMLSERVICE expected max XML output size, required for DB2 
      ilib   (str): optional - XMLSERVICE library compiled (default QXMLSERV)

    Example:
      from itoolkit.db2.idb2call import *
      itransport = iDB2Call(user,password)
      -- or --
      conn = ibm_db.connect(database, user, password)
      itransport = iDB2Call(conn)

    Returns:
       (obj)


    def __init__(self, iuid, ipwd=0, idb2=0, ictl=0, ipc=0, isiz=0, ilib=0):


    def trace_data(self):
        Return trace driver data.

        Args:
          none

        Returns:
          initialization data


    def call(self, itool):
        Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml




class iLibCall:
    
    Transport XMLSERVICE direct job call (within job/process calls).

    Args:
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      iccsid (int): optional - XMLSERVICE EBCDIC CCSID [0,37,...] 0 = default jobccsid (1.2+)
      pccsid (int): optional - XMLSERVICE ASCII CCSID [0,1208, ...] 0 = default 1208 (1.2+)

    Returns:
      none


    def __init__(self, ictl=0, ipc=0, iccsid=0, pccsid=0):


    def trace_data(self):
        Return trace driver data.

        Args:
          none

        Returns:
          initialization data


    def call(self, itool):
        Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml




class iRestCall:
    
    Transport XMLSERVICE calls over standard HTTP rest.

    Args:
      iurl   (str): XMLSERVICE url (https://common1.frankeni.com:47700/cgi-bin/xmlcgi.pgm).
      iuid   (str): Database user profile name
      ipwd   (str): optional - Database user profile password
                               -- or --
                               env var PASSWORD (export PASSWORD=mypass) 
      idb2   (str): optional - Database (WRKRDBDIRE *LOCAL)
      ictl   (str): optional - XMLSERVICE control ['*here','*sbmjob'] 
      ipc    (str): optional - XMLSERVICE xToolkit job route for *sbmjob ['/tmp/myunique42'] 
      isiz   (str): optional - XMLSERVICE expected max XML output size, required for DB2 

    Example:
      from itoolkit.rest.irestcall import *
      itransport = iRestCall(url,user,password)

    Returns:
      none


    def __init__(self, iurl, iuid, ipwd=0, idb2=0, ictl=0, ipc=0, isiz=0):


    def trace_data(self):
        Return trace driver data.

        Args:
          none

        Returns:
          initialization data


    def call(self, itool):
        Call xmlservice with accumulated input XML.

        Args:
          itool  - iToolkit object

        Returns:
          xml

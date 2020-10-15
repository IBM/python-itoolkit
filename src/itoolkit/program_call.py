from .base import iBase


class iPgm (iBase): # noqa N801
    r"""
    IBM i XMLSERVICE call \*PGM.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iname (str): IBM i \*PGM or \*SRVPGM name
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'} : XMLSERVICE error choice {'error':'fast'}
        {'func':'MYFUNC'}       : IBM i \*SRVPGM function export.
        {'lib':'mylib'}         : IBM i library name
        {'mode':'opm|ile'}      : XMLSERVICE error choice {'mode':'ile'}

    Example:
      Example calling the `ZZCALL` program with 5 arguments::

        iPgm('zzcall','ZZCALL')
            .addParm(iData('var1','1a','a'))
            .addParm(iData('var2','1a','b'))
            .addParm(iData('var3','7p4','32.1234'))
            .addParm(iData('var4','12p2','33.33'))
            .addParm(iDS('var5')
                .addData(iData('d5var1','1a','a'))
                .addData(iData('d5var2','1a','b'))
                .addData(iData('d5var3','7p4','32.1234'))
                .addData(iData('d5var4','12p2','33.33'))
            )
    """

    def __init__(self, ikey, iname, iopt={}):
        opts = {
            '_id': ikey,
            '_tag': 'pgm',
            '_value': '',
            'name': iname,
            'error': 'fast'
        }
        super().__init__(iopt, opts)
        self.pcnt = 0

    def addParm(self, obj, iopt={}): # noqa N802
        """Add a parameter child node.

        Args:
          obj   (obj): iData object or iDs object.
          iopt (dict): options to pass to iParm constructor
        """
        self.pcnt += 1
        p = iParm('p' + str(self.pcnt), iopt)
        p.add(obj)
        self.add(p)
        return self


class iSrvPgm (iPgm): # noqa N801
    r"""
    IBM i XMLSERVICE call \*SRVPGM.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      iname (str): IBM i \*PGM or \*SRVPGM name
      ifunc (str): IBM i \*SRVPGM function export.
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
        super().__init__(ikey, iname, iopt)

    def addRet(self, obj): # noqa N802
        """Add a return structure child node.

        Args:
          obj   (obj): iData object or iDs object.
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
            '_id': ikey,
            '_tag': 'parm',
            '_value': '',
            'io': 'both'
        }
        super().__init__(iopt, opts)


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
            '_id': ikey,
            '_tag': 'return',
            '_value': ''
        }
        super().__init__({}, opts)


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
            '_id': ikey,
            '_tag': 'ds',
            '_value': ''
        }
        super().__init__(iopt, opts)

    def addData(self, obj): # noqa N802
        """Add a iData or iDS child node.

        Args:
          obj   (obj): iData object or iDs object.
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
            '_id': ikey,
            '_tag': 'data',
            '_value': str(ival) if ival is not None else "",
            'type': itype
        }
        super().__init__(iopt, opts)

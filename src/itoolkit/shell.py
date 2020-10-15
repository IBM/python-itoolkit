from .base import iBase

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
            '_id': ikey,
            '_tag': 'sh',
            '_value': icmd,
            'error': 'fast'
        }
        super().__init__(iopt, opts)


class iCmd5250(iSh): # noqa N801
    r"""
    IBM i XMLSERVICE call 5250 \*CMD returning \*OUTPUT.

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
        super().__init__(ikey, cmd, iopt)

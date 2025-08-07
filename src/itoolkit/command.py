# Copyright contributors to the python-itoolkit project 
# SPDX-License-Identifier: MIT
from .base import iBase


class iCmd(iBase): # noqa N801
    r"""
    IBM i XMLSERVICE call \*CMD not returning \*OUTPUT.

    Args:
      ikey  (str): XML <ikey>...operation ...</ikey> for parsing output.
      icmd  (str): IBM i command no output (see 5250 command prompt).
      iopt (dict): option - dictionay of options (below)
        {'error':'on|off|fast'}   : XMLSERVICE error option
        {'exec':cmd|system|rexx'} : XMLSERVICE command type {'exec':'cmd'}
        RTVJOBA CCSID(?N)      {'exec':'rex'}

    Example:
      Example calling two CL commands::

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
            '_id': ikey,
            '_tag': 'cmd',
            '_value': icmd,
            'exec': 'rexx' if '?' in icmd else 'cmd',
            'error': 'fast'
        }
        super().__init__(iopt, opts)

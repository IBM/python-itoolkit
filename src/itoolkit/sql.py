# Copyright contributors to the python-itoolkit project 
# SPDX-License-Identifier: MIT
import xml.dom.minidom

from .base import iBase


class SqlBaseAction (iBase):
    def _make(self, doc):
        node = super()._make(doc)

        # Create a surrounding <sql> tag
        sql_node = doc.createElement('sql')
        sql_node.setAttribute('var', self.opt['_id'])
        sql_node.appendChild(node)

        return sql_node

class iSqlQuery (SqlBaseAction): # noqa N801
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
            '_id': ikey,
            '_tag': 'query',
            '_value': isql,
            'error': 'fast'
        }
        super().__init__(iopt, opts)


class iSqlPrepare (SqlBaseAction): # noqa N801
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
            '_id': ikey,
            '_tag': 'prepare',
            '_value': isql,
            'error': 'fast'
        }
        super().__init__(iopt, opts)


class iSqlExecute (SqlBaseAction): # noqa N801
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
            '_id': ikey,
            '_tag': 'execute',
            '_value': '',
            'error': 'fast'
        }
        super().__init__(iopt, opts)
        self.pcnt = 0

    def addParm(self, obj): # noqa N802
        """Add a iSqlParm child node.

        Args:
          obj   (obj): iSqlParm object.
        """
        self.add(obj)
        return self


class iSqlFetch (SqlBaseAction): # noqa N801
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
    """

    def __init__(self, ikey, iopt={}):
        opts = {
            '_id': ikey,
            '_tag': 'fetch',
            '_value': '',
            'block': 'all',
            'error': 'fast'
        }
        super().__init__(iopt, opts)


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
            '_id': ikey,
            '_tag': 'parm',
            '_value': ival,
            'io': 'both'
        }
        super().__init__(iopt, opts)


class iSqlFree (SqlBaseAction): # noqa N801
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
            '_id': ikey,
            '_tag': 'free',
            '_value': '',
            'error': 'fast'
        }
        super().__init__(iopt, opts)

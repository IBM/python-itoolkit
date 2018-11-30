"""
Configure:
  Requires XMSLERVICE library installed, see following link installation 
  http://yips.idevcloud.com/wiki/index.php/XMLService/XMLSERVICE

Transports:
  1) XMLSERVICE direct call (current job)
  from itoolkit.lib.ilibcall import *
  itransport = iLibCall()

  2) XMLSERVICE db2 call (QSQSRVR job)
  from itoolkit.db2.idb2call import *
  itransport = iDB2Call(config.user,config.password)
  -- or --
  conn = ibm_db.connect(database, user, password)
  itransport = iDB2Call(conn)

  3) XMLSERVICE http/rest/web call (Apache job)
  from itoolkit.rest.irestcall import *
  itransport = iRestCall(url, user, password)
"""
from itoolkit.lib.ilibcall import *
itransport = iLibCall()
# itransport = iLibCall("*here *cdata *debug") # i will stop, inquiry message qsysopr


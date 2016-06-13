import config
import ibm_db
from itoolkit.db2.idb2call import *
conn = ibm_db.connect(config.database, config.user, config.password)
if ibm_db.active(conn):
  config.itransport = iDB2Call(conn)
else:
  raise Exception("db2 conn failed: " + ibm_db. conn_errormsg)


from itoolkit import *
from itoolkit.transport import DatabaseTransport
import ibm_db_dbi

conn = ibm_db_dbi.connect()
itransport = DatabaseTransport(conn)

itool = iToolKit()
itool.add(
 iPgm('zzcall','ZZCALLNOT')
 .addParm(iData('INCHARA','1a','a'))
 )

# xmlservice write trace log to *terminal
itool.trace_open()
itool.call(itransport)
itool.trace_close()

zzcall = itool.dict_out('zzcall')
if 'success' in zzcall:
  print (zzcall['success'])
else:
  print (zzcall['error'])
  exit()



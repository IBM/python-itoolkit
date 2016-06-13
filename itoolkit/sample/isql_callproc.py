import config
from itoolkit import *

itool = iToolKit(iparm=1)
sql  = "DROP PROCEDURE XMLSERVICE/FLUBBER\n"
itool.add(iSqlQuery('crt', sql))
itool.add(iSqlFree('free0'))
sql = "CREATE PROCEDURE XMLSERVICE/FLUBBER(IN first_name VARCHAR(128), INOUT any_name VARCHAR(128))\n"
sql += "LANGUAGE SQL\n"
sql += "BEGIN\n"
sql += "SET any_name = 'Flubber';\n"
sql += "END\n"
itool.add(iSqlQuery('crt', sql))
itool.add(iSqlFree('free1'))
itool.add(iSqlPrepare('callflubber', "call XMLSERVICE/FLUBBER(?,?)"))
itool.add(
 iSqlExecute('exec')
 .addParm(iSqlParm('myin','Jones'))
 .addParm(iSqlParm('myout','jjjjjjjjjjjjjjjjjjjjjuuuuuuuuuuuuuuuunnnnnnnnnkkkkkkkkkkkk'))
)
itool.add(iSqlFree('free2'))
# print(itool.xml_in())
# exit()

# xmlservice
itool.call(config.itransport)
# print(itool.xml_out())

# output
FLUBBER = itool.dict_out('exec')
if 'error' in FLUBBER:
  print (FLUBBER['error'])
  exit()
else:
  print ('myout = ' + FLUBBER['myout']['data'])


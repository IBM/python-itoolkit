# RTVJOBA can't issue from command line,
# but works with itoolkit
import config
from itoolkit import *

# modify iToolKit not include row node
itool = iToolKit(iparm=0, iret=0, ids=1, irow=0)
itool.add(iCmd('rtvjoba', 'RTVJOBA USRLIBL(?) SYSLIBL(?) CCSID(?N) OUTQ(?)'))

# xmlservice
itool.call(config.itransport)

# output
rtvjoba = itool.dict_out('rtvjoba')
print (rtvjoba)
if 'error' in rtvjoba:
  print (rtvjoba['error'])
  exit()
else:
  print('USRLIBL = ' + rtvjoba['USRLIBL'])
  print('SYSLIBL = ' + rtvjoba['SYSLIBL'])
  print('CCSID   = ' + rtvjoba['CCSID'])
  print('OUTQ    = ' + rtvjoba['OUTQ'])


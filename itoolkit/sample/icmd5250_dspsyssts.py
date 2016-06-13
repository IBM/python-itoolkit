#                                                                         Bottom
# Type command, press Enter.
# ===> dspsyssts                                                                 
#                             Display System Status                     LP0364D
#                                                             06/22/15  15:22:28
# % CPU used . . . . . . . :         .1    Auxiliary storage:
# Elapsed time . . . . . . :   00:00:01      System ASP . . . . . . :    176.2 G
# Jobs in system . . . . . :        428      % system ASP used  . . :    75.6481
import config
from itoolkit import *

itool = iToolKit()
itool.add(iCmd5250('dspsyssts', 'dspsyssts'))

# xmlservice
itool.call(config.itransport)

# output
dspsyssts = itool.dict_out('dspsyssts')
if 'error' in dspsyssts:
  print (dspsyssts['error'])
  exit()
else:
  print (dspsyssts['dspsyssts'])


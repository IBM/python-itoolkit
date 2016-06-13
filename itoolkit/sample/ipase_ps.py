# > ps -ef
#      UID   PID  PPID   C    STIME    TTY  TIME CMD
#  qsecofr    12    11   0   May 08      -  8:33 /QOpenSys/QIBM/ProdData/JavaVM/jdk60/32bit/jre/lib/ppc/jvmStartPase 566 
# qtmhhttp    31     1   0   May 08      -  0:00 /usr/local/zendsvr/bin/watchdog -c /usr/local/zendsvr/etc/watchdog-monitor.ini -s monitor 
import config
from itoolkit import *

itool = iToolKit()
itool.add(iSh('ps', 'ps -ef'))

# xmlservice
itool.call(config.itransport)

# output
ps = itool.dict_out('ps')
if 'error' in ps:
  print (ps['error'])
  exit()
else:
  print (ps['ps'])


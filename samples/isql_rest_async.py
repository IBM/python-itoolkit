try:
  import queue
except ImportError:
  import Queue as queue
import threading
import urllib
from itoolkit.transport import HttpTransport
from itoolkit import *
class iDB2Async():
  def __init__(self, isql):
      self.itran = HttpTransport('http://yips.idevcloud.com/cgi-bin/xmlcgi.pgm','*NONE','*NONE')
      self.itool = iToolKit()
      self.itool.add(iSqlQuery('iqry', isql))
      self.itool.add(iSqlFetch('ifch'))
      self.itool.add(iSqlFree('ifre'))
  def go(self):
      self.itool.call(self.itran)
      return self.itool.dict_out('ifch')
def get_url(q, icmd):
    q.put(iDB2Async(icmd).go())
thedb2s = ["select CUSNUM from QIWS/QCUSTCDT where LSTNAM='Jones'", 
          "select CUSNUM from QIWS/QCUSTCDT where LSTNAM='Johnson'"]
q = queue.Queue()
for u in thedb2s:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()
# q.join()
for u in thedb2s:
    s = q.get()
    print(s)


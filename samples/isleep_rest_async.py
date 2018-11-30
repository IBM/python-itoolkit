try:
  import queue
except ImportError:
  import Queue as queue
import threading
import urllib
from itoolkit.transport import HttpTransport
from itoolkit import *
class iShSleep():
  def __init__(self, icmd):
      self.itran = HttpTransport('http://yips.idevcloud.com/cgi-bin/xmlcgi.pgm','*NONE','*NONE')
      self.itool = iToolKit()
      self.itool.add(iSh('igo',icmd))
  def go(self):
      self.itool.call(self.itran)
      return self.itool.dict_out('igo')
def get_url(q, icmd):
    q.put(iShSleep(icmd).go())
theshs = ["echo 'thing 1==>';date;sleep 10;date", 
          "echo 'thing 2==>';date;sleep 5;date"]
q = queue.Queue()
for u in theshs:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()
# q.join()
for u in theshs:
    s = q.get()
    print(s)


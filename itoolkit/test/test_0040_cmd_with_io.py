import unittest
from itoolkit import *
import config

class ToolkitTest(unittest.TestCase):
  # This function is called to run all the tests.
  def runTest(self):
    # modify iToolKit not include row node
    itool = iToolKit(iparm=0, iret=0, ids=1, irow=0)
    itool.add(iCmd('rtvjoba', 'RTVJOBA USRLIBL(?) SYSLIBL(?) CCSID(?N) OUTQ(?)'))
    itool.call(config.itransport)
    rtvjoba = itool.dict_out('rtvjoba')
    self.assertTrue(rtvjoba['success'])
    if 'success' in rtvjoba:
      self.assertTrue(rtvjoba['USRLIBL'])
      self.assertTrue(rtvjoba['SYSLIBL'])
      self.assertTrue(rtvjoba['CCSID'])
      self.assertTrue(rtvjoba['OUTQ'])

obj = ToolkitTest()
suite = obj.runTest()


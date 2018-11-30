import unittest
from itoolkit import *
import config

class ToolkitTest(unittest.TestCase):
  # This function is called to run all the tests.
  def runTest(self):
    # modify iToolKit not include row node
    itool = iToolKit()
    itool.add(iCmd('cmderror', 'CHGLIBL LIBL(FROGLEG) CURLIB(TOADLEG)'))
    itool.call(config.itransport)
    cmderror = itool.dict_out('cmderror')
    # print(cmderror)
    self.assertTrue(cmderror['error'])

obj = ToolkitTest()
suite = obj.runTest()


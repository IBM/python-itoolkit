import unittest
from itoolkit import *
import config

class ToolkitTest(unittest.TestCase):
  # This function is called to run all the tests.
  def runTest(self):
    # modify iToolKit not include row node
    itool = iToolKit()
    itool.add(
     iPgm('zzcall','ZZCALLNOT')
     .addParm(iData('INCHARA','1a','a'))
     .addParm(iData('INCHARB','1a','b'))
     .addParm(iData('INDEC1','7p4','32.1234'))
     .addParm(iData('INDEC2','12p2','33.33'))
     )
    itool.call(config.itransport)
    cmderror = itool.dict_out('cmderror')
    # print(cmderror)
    self.assertTrue(cmderror['error'])

obj = ToolkitTest()
suite = obj.runTest()


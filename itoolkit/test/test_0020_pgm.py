# XMLSERVICE/ZZCALL:
#     D  INCHARA        S              1a
#     D  INCHARB        S              1a
#     D  INDEC1         S              7p 4        
#     D  INDEC2         S             12p 2
#     D  INDS1          DS                  
#     D   DSCHARA                      1a
#     D   DSCHARB                      1a           
#     D   DSDEC1                       7p 4      
#     D   DSDEC2                      12p 2            
#      *+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#      * main(): Control flow
#      *+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     C     *Entry        PLIST                   
#     C                   PARM                    INCHARA
#     C                   PARM                    INCHARB
#     C                   PARM                    INDEC1
#     C                   PARM                    INDEC2
#     C                   PARM                    INDS1
import unittest
from itoolkit import *
import config

class ToolkitTest(unittest.TestCase):
  # This function is called to run all the tests.
  def runTest(self):
    itool = iToolKit()
    itool.add(iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE) CURLIB(XMLSERVICE)'))
    itool.add(
     iPgm('zzcall','ZZCALL')
     .addParm(iData('INCHARA','1a','a'))
     .addParm(iData('INCHARB','1a','b'))
     .addParm(iData('INDEC1','7p4','32.1234'))
     .addParm(iData('INDEC2','12p2','33.33'))
     .addParm(
      iDS('INDS1')
      .addData(iData('DSCHARA','1a','a'))
      .addData(iData('DSCHARB','1a','b'))
      .addData(iData('DSDEC1','7p4','32.1234'))
      .addData(iData('DSDEC2','12p2','33.33'))
      )
     )
    itool.call(config.itransport)
    chglibl = itool.dict_out('chglibl')
    zzcall = itool.dict_out('zzcall')
    self.assertTrue(chglibl['success'])
    self.assertTrue(zzcall['success'])
    if 'success' in zzcall:
      self.assertEqual(zzcall['INCHARA'],'C')
      self.assertEqual(zzcall['INCHARB'],'D')
      self.assertEqual(zzcall['INDEC1'],'321.1234')
      self.assertEqual(zzcall['INDEC2'],'1234567890.12')
      self.assertEqual(zzcall['INDS1']['DSCHARA'],'E')
      self.assertEqual(zzcall['INDS1']['DSCHARB'],'F')
      self.assertEqual(zzcall['INDS1']['DSDEC1'],'333.3330')
      self.assertEqual(zzcall['INDS1']['DSDEC2'],'4444444444.44')

obj = ToolkitTest()
suite = obj.runTest()


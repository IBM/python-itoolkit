#     D ARRAYMAX        c                   const(999)
#     D dcRec_t         ds                  qualified based(Template)
#     D  dcMyName                     10A
#     D  dcMyJob                    4096A
#     D  dcMyRank                     10i 0
#     D  dcMyPay                      12p 2
#      *+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#      * zzarray: check return array aggregate 
#      *+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     P zzarray         B                   export
#     D zzarray         PI                  likeds(dcRec_t) dim(ARRAYMAX)
#     D  myName                       10A
#     D  myMax                        10i 0
#     D  myCount                      10i 0
import unittest
from itoolkit import *
import config

class ToolkitTest(unittest.TestCase):
  # This function is called to run all the tests.
  def runTest(self):
    itool = iToolKit()
    itool.add(iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE)'))
    itool.add(
     iSrvPgm('zzarray','ZZSRV','ZZARRAY')
     .addParm(iData('myName','10a','ranger'))
     .addParm(iData('myMax','10i0','8'))
     .addParm(iData('myCount','10i0','',{'enddo':'mycnt'}))
     .addRet(
      iDS('dcRec_t',{'dim':'999','dou':'mycnt'})
      .addData(iData('dcMyName','10a',''))
      .addData(iData('dcMyJob','4096a',''))
      .addData(iData('dcMyRank','10i0',''))
      .addData(iData('dcMyPay','12p2',''))
      )
     )
    itool.call(config.itransport)
    chglibl = itool.dict_out('chglibl')
    zzarray = itool.dict_out('zzarray')
    self.assertTrue(chglibl['success'])
    self.assertTrue(zzarray['success'])
    if 'success' in zzarray:
      self.assertEqual(zzarray['myName'],'ranger')
      self.assertEqual(zzarray['myMax'],'8')
      self.assertEqual(zzarray['myCount'],'8')
      i = 1
      dcRec_t = zzarray['dcRec_t']
      for rec in dcRec_t:
        self.assertEqual(rec['dcMyName'],"ranger"+str(i))
        self.assertEqual(rec['dcMyJob'],"Test 10"+str(i))
        self.assertEqual(int(rec['dcMyRank']), 10 + i)
        self.assertEqual(float(rec['dcMyPay']),13.42 * i)
        i+=1

obj = ToolkitTest()
suite = obj.runTest()


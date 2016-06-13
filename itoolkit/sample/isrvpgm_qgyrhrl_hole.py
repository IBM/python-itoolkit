import config
from itoolkit import *
# Retrieve Hardware Resource List (QGYRHRL, QgyRtvHdwRscList) API
# Service Program: QGYRHR
# Default Public Authority: *USE
# Threadsafe: No
# Required Parameter Group:
#  Output Char(*)..............Receiver variable (RHRL0100, RHRL0110)
#  Input Binary(4).............Length of receiver variable
#  Input Char(8)...............Format name
#  Input Binary(4).............Resource category (see hardware resource category)
#  I/O Char(*).................Error code
# RHRL0100 Format
#  BINARY(4)...................Bytes returned
#  BINARY(4)...................Bytes available
#  BINARY(4)...................Number of resources returned
#  BINARY(4)...................Length of resource entry
#  CHAR(*).....................Resource entries
#  These fields repeat for each resource.
#  BINARY(4)...................Resource category
#  BINARY(4)...................Family level
#  BINARY(4)...................Line type
#  CHAR(10)....................Resource name
#  CHAR(4).....................Type number
#  CHAR(3).....................Model number
#  CHAR(1).....................Status
#  CHAR(8).....................System to which adapter is connected
#  CHAR(12)....................Adapter address
#  CHAR(50)....................Description
#  CHAR(24)....................Resource kind (liar, liar, pants on fire ... binary, not char)
#  hardware resource category:
#  1  All hardware resources (does not include local area network resources)
#  2  Communication resources
#  3  Local work station resources
#  4  Processor resources
#  5  Storage device resources
#  6  Coupled system adapter resources
#  7  Local area network resources
#  8  Cryptographic resources
#  9  Tape and optical resources
#  10 Tape resources
#  11 Optical resources
itool = iToolKit()
itool.add(
 iSrvPgm('qgyrhr','QGYRHR','QgyRtvHdwRscList')
 .addParm(
  iDS('RHRL0100_t',{'len':'rhrlen'})
  .addData(iData('rhrRet','10i0',''))
  .addData(iData('rhrAvl','10i0',''))
  .addData(iData('rhrNbr','10i0','',{'enddo':'mycnt'}))
  .addData(iData('rhrLen','10i0',''))
  .addData(iDS('res_t',{'dim':'999','dou':'mycnt'})
           .addData(iData('resCat','10i0',''))
           .addData(iData('resLvl','10i0',''))
           .addData(iData('resLin','10i0',''))
           .addData(iData('resNam','10a',''))
           .addData(iData('resTyp','4a',''))
           .addData(iData('resMod','3a',''))
           .addData(iData('resSts','1a',''))
           .addData(iData('resSys','8a',''))
           .addData(iData('resAdp','12a',''))
           .addData(iData('resDsc','50h','')) # was 50a
           .addData(iData('resKnd','24h','')) # was 24b
           )
 )
 .addParm(iData('rcvlen','10i0','',{'setlen':'rhrlen'}))
 .addParm(iData('fmtnam','10a','RHRL0100'))
 .addParm(iData('rescat','10i0','3')) #  3  Local work station resources
 .addParm(
  iDS('ERRC0100_t',{'len':'errlen'})
  .addData(iData('errRet','10i0',''))
  .addData(iData('errAvl','10i0',''))
  .addData(iData('errExp','7A','',{'setlen':'errlen'}))
  .addData(iData('errRsv','1A',''))
 )
)
# xmlservice
itool.call(config.itransport)
#output
qgyrhr = itool.dict_out('qgyrhr')
if 'success' in qgyrhr:
  print (qgyrhr['success'])
  print ("    Length of receiver variable......" + qgyrhr['rcvlen'])
  print ("    Format name......................" + qgyrhr['fmtnam'])
  print ("    Resource category................" + qgyrhr['rescat'])
  RHRL0100_t = qgyrhr['RHRL0100_t']
  print ('    RHRL0100_t:')
  print ("      Bytes returned................." + RHRL0100_t['rhrRet'])
  print ("      Bytes available................" + RHRL0100_t['rhrAvl'])
  print ("      Number of resources returned..." + RHRL0100_t['rhrNbr'])
  print ("      Length of resource entry......." + RHRL0100_t['rhrLen'])
  if int(RHRL0100_t['rhrNbr']) > 0:
    res_t = RHRL0100_t['res_t']
    for rec in res_t:
      print ("        --------------------------------------------------------")
      keys = rec.keys()
      print ("        Resource category............" + rec['resCat'])
      print ("        Family level................." + rec['resLvl'])
      print ("        Line type...................." + rec['resLin'])
      print ("        Resource name................" + rec['resNam'])
      print ("        Type number.................." + rec['resTyp'])
      print ("        Model number................." + rec['resMod'])
      print ("        Status......................." + rec['resSts'])
      print ("        System adapter connected....." + rec['resSys'])
      print ("        Adapter address.............." + rec['resAdp'])
      print ("        Description.................." + rec['resDsc'])
      print ("        Resource kind................" + rec['resKnd'])
else:
  print (qgyrhr['error'])
  exit()


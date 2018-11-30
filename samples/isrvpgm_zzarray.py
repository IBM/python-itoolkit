import config
from itoolkit import *
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

# xmlservice
itool.call(config.itransport)

# output
# print(itool.xml_out())
chglibl = itool.dict_out('chglibl')
if 'success' in chglibl:
  print (chglibl['success'])
else:
  print (chglibl['error'])
  exit()

zzarray = itool.dict_out('zzarray')
# print(zzarray)
if 'success' in zzarray:
  print (zzarray['success'])
  print ("    myName       : " + zzarray['myName'])
  print ("    myMax        : " + zzarray['myMax'])
  print ("    myCount      : " + zzarray['myCount'])
  dcRec_t = zzarray['dcRec_t']
  for rec in dcRec_t:
    print ('    dcRec_t:')
    print ("      dcMyName : " + rec['dcMyName'])
    print ("      dcMyJob  : " + rec['dcMyJob'])
    print ("      dcMyRank : " + rec['dcMyRank'])
    print ("      dcMyPay  : " + rec['dcMyPay'])
else:
  print (zzarray['error'])
  exit()



import config
from itoolkit import *
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
itool = iToolKit()
itool.add(iCmd('chglibl', 'CHGLIBL LIBL(XMLSERVICE)'))
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

# xmlservice
itool.call(config.itransport)

# output
chglibl = itool.dict_out('chglibl')
if 'success' in chglibl:
  print (chglibl['success'])
else:
  print (chglibl['error'])
  exit()

zzcall = itool.dict_out('zzcall')
if 'success' in zzcall:
  print (zzcall['success'])
  print ("    INCHARA      : " + zzcall['INCHARA'])
  print ("    INCHARB      : " + zzcall['INCHARB'])
  print ("    INDEC1       : " + zzcall['INDEC1'])
  print ("    INDEC2       : " + zzcall['INDEC2'])
  print ("    INDS1.DSCHARA: " + zzcall['INDS1']['DSCHARA'])
  print ("    INDS1.DSCHARB: " + zzcall['INDS1']['DSCHARB'])
  print ("    INDS1.DSDEC1 : " + zzcall['INDS1']['DSDEC1'])
  print ("    INDS1.DSDEC2 : " + zzcall['INDS1']['DSDEC2'])
else:
  print (zzcall['error'])
  exit()



from itoolkit import *
from itoolkit.transport import DirectTransport

print("********************")
print("********************")
print("Hey user,")
print("Using '*debug' transport parameter allows debug halt before run.")
print ("\n  itransport = DirectTransport('*here *debug')\n")
print("Expect qsysopr inquire message, you must answer to continue script.")
print("You may attach a debugger before you answer the inquiry.")
print("\n  dspmsg qsysopr\n")
print("  Reply inquiry message any character.")
print("    From  . . . :   ADC            06/25/15   14:08:07")
print("    Debug client 362262/QSECOFR/QP0ZSPWP")
print("      Reply . . :   c\n")
print("Script continues to run after answer (call PGM, etc.)")
print("********************")
print("********************")

itransport = DirectTransport("*here *debug") # i will stop, inquiry message qsysopr
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
itool.call(itransport)

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



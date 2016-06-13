import config
from itoolkit import *
# XMLSERVICE/ZZSRV.ZZVARY:
#     P zzvary          B                   export
#     D zzvary          PI            20A   varying
#     D  myName                       10A   varying
itool = iToolKit()
itool.add(iXml("<cmd var='chglibl'>CHGLIBL LIBL(XMLSERVICE)</cmd>"))
myxml  = "<pgm name='ZZSRV' func='ZZVARY' var='zzvary'>"
myxml += "<parm io='in'>"
myxml += "<data var='myName' type='10A' varying='on'><![CDATA[<Ranger>]]></data>"
myxml += "</parm>"
myxml += "<return>"
myxml += "<data var='myNameis' type='20A' varying='on'><![CDATA[<Mud>]]></data>"
myxml += "</return>"
myxml += "</pgm>"
itool.add(iXml(myxml))

# xmlservice
itool.call(config.itransport)

# output
chglibl = itool.dict_out('chglibl')
if 'success' in chglibl:
  print (chglibl['success'])
else:
  print (chglibl['error'])
  exit()

zzvary = itool.dict_out('zzvary')
if 'success' in zzvary:
  print (zzvary['success'])
  # print ("    myName       : " + zzvary['myName']) ... input only, no output
  print ("    myNameis     : " + zzvary['myNameis'])
else:
  print (zzvary['error'])
  exit()



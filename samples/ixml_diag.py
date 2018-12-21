import config
from itoolkit import *

# from itoolkit.transport import DirectTransport
# itransport = DirectTransport("*here *debug") # i will stop, inquiry message qsysopr

itool = iToolKit()
itool.add(iCmd('chglibl2', 'CHGLIBL LIBL(QTEMP XMLSERVICE)'))
itool.add(iCmd('chglibl3', 'CHGLIBL LIBL(SOMEBAD42)'))
myxml  = "<diag/>"
itool.add(iXml(myxml))

print(itool.xml_in())


# xmlservice
itool.call(config.itransport)
# itool.call(itransport)

# output
print(itool.xml_out())
diag = itool.dict_out()
if 'version' in diag: 
  print ("version   : "+diag['version'])
print ("job       : "+diag['jobnbr']+'/'+diag['jobuser']+'/'+diag['jobname'])
print ("jobipc    : "+diag['jobipc'])
print ("curuser   : "+diag['curuser'])
print ("ccsid     : "+diag['ccsid'])
print ("dftccsid  : "+diag['dftccsid'])
print ("paseccsid : "+diag['paseccsid'])
print ("syslibl   : "+diag['syslibl'])
print ("usrlibl   : "+diag['usrlibl'])
joblog = diag['joblog'].replace("\n"," ")
cpflist = ""
for word in joblog.split(' '):
  if word[:3] == 'CPF' or word[:3] == 'MCH':
    cpflist += word + " "
    if diag['jobcpf'] == "":
       diag['jobcpf'] = word
print ("jobcpf    : "+diag['jobcpf'] + " ( " + cpflist + ")")
print ("joblog    :\n" + diag['joblog'])


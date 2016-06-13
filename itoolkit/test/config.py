import os
test_dir='.'
database='*LOCAL'
user	='DB2'
password='NICE2DB2'
url='http://lp0364d/cgi-bin/xmlcgi.pgm'
# see tests.py
itransport=None
itransv=os.getenv('TRANSPORT', 'lib')
if itransv == 'lib':
  import itool400
elif itransv == 'rest':
  import itoolrest
elif itransv == 'db2':
  import itooldb2
elif itransv == 'db2e':
  import itooldb2existing


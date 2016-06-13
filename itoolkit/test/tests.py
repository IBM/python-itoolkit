import os, sys, traceback, subprocess

print("\n*******************************\nChecking transports ...\n*******************************\n")
try:
  import itool400
  skip400 = 'itool400.py'
except:
  skip400 = False
  traceback.print_exc()

try:
  import itoolrest
  skiprest = 'itoolrest.py'
except:
  skiprest = False
  traceback.print_exc()

try:
  import itooldb2
  skipdb2 = 'itooldb2.py'
except:
  skipdb2 = False
  traceback.print_exc()

if skip400:
  os.putenv('TRANSPORT', 'lib')
  print("\n*******************************\nRunning unittest (lib) ...\n*******************************\n")
  subprocess.call(["python", "rerun.py"])

if skiprest:
  os.putenv('TRANSPORT', 'rest')
  print("\n*******************************\nRunning unittest (rest) ...\n*******************************\n")
  subprocess.call(["python", "rerun.py"])

if skipdb2:
  os.putenv('TRANSPORT', 'db2')
  print("\n*******************************\nRunning unittest (db2) ...\n*******************************\n")
  subprocess.call(["python", "rerun.py"])


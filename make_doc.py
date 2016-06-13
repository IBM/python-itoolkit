import os
# class documentation
wiki_idx = ''
wiki_doc = "!!! IBM project link\n"
wiki_doc += "* [[https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/Python]]\n"
wiki_doc += "\n!!! Overview\n"
wiki_table = ''
wiki_table += "(:table border=1 width=100%:)\n"
wiki_table += "(:cellnr colspan=2 align=center style='background-color: #CCCCCC;':)[++Index++]\n"
wiki_table += "(:cellnr:)[++Classes++]\n"
wiki_table += "(:cell:)[++Sample++]\n"

man_doc = ''
first = True
intro = True
for root, dirs, files in os.walk("itoolkit/"):
  # not included in documentation
  if "/test" in root:
    continue   
  if "/sample" in root:
    continue   
  if "/doc" in root:
    continue 
  # look for .py files
  files.sort()
  for file in files:
    if "__init__" in file:
      continue
    if file.endswith(".py"):
      if "itoolkit" in file:
        klass = True
      else:
        klass = False
      fn = os.path.join(root, file)
      f = open(fn,"r")
      go = False
      body = ''
      man_doc += "\n\n"
      for line in f:
        # start/end body text
        if '"""' in line:
          if go:
            # output body
            if klass:
              man_doc += body
              if intro:
                wiki_doc += "\n[@\n"
              wiki_doc += body
              if intro:
                wiki_doc += "\n@]\n"
              intro = False
            body = ''
            go = False
            klass = False
          else:
            go = True
            p = line.split('"""')
            body = p[0] + p[1]
            continue
        # collect body text
        if go:
          body += line
        else:
          # output class
          if "class" in line and ":" in line:
            man_doc += "\n\n" + line
            klass = True
            # [[#iBase|iBase]]
            p1 = line.split()
            p2 = p1[1].split('(')
            p3 = p2[0].split(':')
            wiki_idx += "[[#"+p3[0]+"|"+p3[0]+"]]\n"
            if not first:
              wiki_doc += "\n@]\n"
            first = False
            p1 = line.split(':')
            wiki_doc += "\n[[#"+p3[0]+"]]\n!!! " + p1[0]
            wiki_doc += "\n[@\n"
          # output def
          if "def" in line and ":" in line:
            man_doc += "\n\n" + line
            wiki_doc += "\n\n" + line
            klass = True
wiki_doc += "\n@]"
# sample documentation
wiki_sample_idx = ''
wiki_sample_doc = ''
man_sample = "\n\n"
man_sample += "****************************\n"
man_sample += "****************************\n"
man_sample += "****************************\n"
man_sample += "Samples\n"
man_sample += "****************************\n"
man_sample += "****************************\n"
man_sample += "****************************\n"
man_sample += "\n\n"
for root, dirs, files in os.walk("itoolkit/"):
  # not included in documentation
  if not "/sample" in root:
    continue   
  # look for .py files 
  files.sort()
  for file in files:
    if file.endswith(".py"):
      fn = os.path.join(root, file)
      f = open(fn,"r")
      p = fn.split('/')
      wiki_sample_idx += "[[#"+p[2]+"|"+p[2]+"]]\n"
      man_sample += "\n\n"
      man_sample += "---------------------------------\n"
      man_sample += fn+"\n"
      man_sample += "---------------------------------\n"
      wiki_sample_doc += "\n[[#"+p[2]+"]]\n!!! " + fn + "\n"
      wiki_sample_doc += "[@\n"
      for line in f:
        man_sample += line
        wiki_sample_doc += line
      wiki_sample_doc += "\n@]\n"

# output
with open("itoolkit/doc/README", "w") as text_file:
    text_file.write(man_doc)

wiki_table += "\n(:cellnr:)\n" + wiki_idx
wiki_table += "(:cell:)\n" + wiki_sample_idx
wiki_table += "\n(:tableend:)\n"

print(wiki_table)
print(wiki_doc)
print(wiki_sample_doc)



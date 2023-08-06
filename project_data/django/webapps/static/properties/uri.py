#!/usr/bin/python3
import re


with open('uriworkermap.properties') as f:
   for x in f :
      if re.match('^#|^$', x) : 
         continue
      m =re.search('^\/(.*)\*=(.*)$',x) 
      app,tc = m.group(1),m.group(2).split(';')[0]
      print(f" app = {app}  tc = {tc}")#      
#      print(m.group(1),m.group(2))

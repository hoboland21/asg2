from django.core.files import File
from webapi.models import *
from webapps.settings import *
import re
import requests
import os
import time
import subprocess



TCLIST = ("TC01", "TC02", "TC03", "TC04", "TC05", "TC06", "TC07", "TC08", "TC09","TC10" )

# ENVLIST Display,server,authlvl

ENVLIST = [
    ("STG","rh-stg-01",3),
    ("STG2","rh-stg2-01",3),
    ("STG3","rh-stg3-01",3),
    ("STG3-02","rh-stg3-02",3),
    ("ST","rh-st-01",2),
    ("ST2","rh-st2-01",2),
    ("ST3","rh-st3-01",2),

    ("MO","rh-mo-01",2),
    ("MO2","rh-mo2-01",2),
    ("MO3","rh-mo3-01",2),
    ("MO3-02","rh-mo3-02",2),
    ("PRD","rh-prd-01",1),
    ("PRD-02","rh-prd-02",1) ,
    ("DRC","rh-drc-01",1),
     ]
tcpasswd = "Scr6t7ny"
env_dict =   {x[0]:x[1] for x in ENVLIST }
domain="pdx.odshp.com"

#--------------------
def read_uriworker() :
#--------------------
    result = {}
    uri_file_path = os.path.join(BASE_DIR,'static/properties/uriworkermap.properties')
    with open(uri_file_path,"r") as f:
        for x in f :
            if re.match('^#|^$', x) : 
                continue
            m =re.search('^\/(.*)\*=(.*)',x) 
            app,tc = m.group(1),m.group(2).split(';')[0]
            #print(f" app = {app}  tc = {tc}")
            if tc.upper() not in result :
                result[tc.upper()] = []
            result[tc.upper()].append(app)
    return result      


#--------------------
def env_uriworker(env) :
#--------------------
    result = {}
    user = "tcadminx"
    if env in ("PRD","DRC","PRD-02") :
        user = "tcadmin"
    sshcmd =  f"/usr/bin/sshpass -p {tcpasswd} /usr/bin/ssh  -o StrictHostKeyChecking=no {user}@{env_dict[env]}.pdx.odshp.com "

    cf= f"{sshcmd} cat /etc/httpd/conf/uriworkermap.properties"
    uri,error = run_process(cf)
    
    for x in uri.split('\n'):
        if re.match('^#|^$', x) : 
            continue
        m =re.search('^\/(.*)\*=(.*)',x) 
        app,tc = m.group(1),m.group(2).split(';')[0]
        #print(f" app = {app}  tc = {tc}")
        if tc.upper() not in result :
            result[tc.upper()] = []
        result[tc.upper()].append(app)
    return result


#--------------------
def run_process(cmd_str)	:
#--------------------
    sp = subprocess.Popen(cmd_str,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=sp.communicate()
    return out.decode("UTF-8"),err.decode("UTF-8")

#--------------------
def ssh_cmd(env_name) :
#--------------------
    user = "tcadminx"
    if env_name in ("PRD","DRC","PRD-02") :
        user = "tcadmin"
    return f"/usr/bin/sshpass -p {tcpasswd} /usr/bin/ssh  -o StrictHostKeyChecking=no {user}@{env_dict[env_name]}.pdx.odshp.com "




'''
    result = {}
    user = "tcadminx"
    if env in ("PRD","DRC","PRD-02") :
        user = "tcadmin"
    sshcmd =  f"/usr/bin/sshpass -p {tcpasswd} /usr/bin/ssh  -o StrictHostKeyChecking=no {user}@{env_dict[env]}.pdx.odshp.com "

/usr/bin/jstack

#--------------------
def stack_trace(env_name) :
#--------------------
    run_process(f"{ssh_cmd(env_name)} /opt/tomcat-home/sbin/{cmd}")


'''



#--------------------
def run_cmd(env_name,cmd) :
#--------------------
    # returns message,error
    print(f'RUNNING COMMAND {env_name} {cmd}')
    return run_process(f"{ssh_cmd(env_name)} /opt/tomcat-home/sbin/{cmd}")





# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.html import escape
import requests
import os
import time
import subprocess

from .tools.misc import *


domain="pdx.odshp.com"

# Create your models here.

#========================================
class Logs(models.Model) :
#========================================
    name    =  models.CharField(max_length=80,blank=True)
    type    =  models.CharField(max_length=20,blank=True)
    action  =  models.CharField(max_length=80,blank=True)
    status  =  models.CharField(max_length=80,blank=True)
    label   =  models.CharField(max_length=80,blank=True)
    username=  models.CharField(max_length=128,blank=True)
    time    =  models.CharField(max_length=128,blank=True)

#========================================
class Env(models.Model) :
#========================================
    name    =  models.CharField(max_length=80)
    server  = models.CharField(max_length=80)
    url     = models.CharField(max_length=128)
    color   = models.CharField(max_length=80, default="#FFFFFF")
    authlvl  = models.IntegerField(default=1)

    #-----
    def status(self) :
    #-----
        return os.system(f"ping  -c 1 -w2 {self.server}.{domain} > /dev/null 2>&1")

    #-----
    def start(self) :
    #-----
        return run_cmd(self.name,"PID_start_all.sh &")

    #-----
    def stop(self) :
    #-----
        return run_cmd(self.name,"PID_stop_all.sh &")
    #--------------------
    def ssh_cmd(self) :
        #--------------------
        user = "tcadminx"
        if self.name in ("PRD","DRC","PRD-02") :
            user = "tcadmin"
        return f"/usr/bin/sshpass -p {tcpasswd} /usr/bin/ssh  -o StrictHostKeyChecking=no {user}@{env_dict[self.name]}.pdx.odshp.com "


    #-----
    def logsize(self) :
    #-----
        log = []
        total = 0
        for indx in range(1,11) :
            i = str(indx).zfill(2)
            self.command = f"{self.ssh_cmd()} du -s /opt/tomcat-base-{i}/logs/"
            res = run_process(self.command)[0].split('\t')
            if len(res) < 2 :
                res[0] = 0
            log.append([f'TC{i}',res[0]])
            total += int(res[0])
        log.append(["Total",total])
        return log


#========================================
class TC (models.Model) :
#========================================
    name    =  models.CharField(max_length=20)
    env     =  models.ForeignKey(Env,on_delete=models.CASCADE)
    color   = models.CharField(max_length=80, default="#FFFFFF")
    #-----
    def port(self) :
    #-----
        p = int(self.name[-2:])
        p += 8080
        return str(p)

    #-------------------
    def tc_manager(self,cmd) :
    #-------------------
        try:
            res = requests.get(f"{self.env.url}:{self.port()}/manager/{cmd}",auth=("deployer","tcmoda"),timeout=(1))
        except :
            return "ERROR"
        else:
            return res.text.split('\n')



   #-----
    def status(self) :
        #-----
        try:
            res = requests.get(f"{self.env.url}:{self.port()}/manager/text/list",auth=("deployer","tcmoda"),timeout=(1))
        except :
            return "ERROR"
        else:
            return res.text.split('\n')
    #-----
    def stats(self) :
        #-----
        try:
            res = requests.get(f"{self.env.url}:{self.port()}/manager/status/all",auth=("deployer","tcmoda"),timeout=(1))
        except :
            return "ERROR"
        else:
            return res

    #--------------------
    def ssh_cmd(self) :
        #--------------------
        user = "tcadminx"
        if self.env.name in ("PRD","DRC","PRD-02") :
            user = "tcadmin"
        return f"/usr/bin/sshpass -p {tcpasswd} /usr/bin/ssh  -o StrictHostKeyChecking=no {user}@{env_dict[self.env.name]}.pdx.odshp.com "


    #--------------------
    def logsize(self) :
        #--------------------
        self.command = f"{self.ssh_cmd()} du -sh /opt/tomcat-base-{self.name[2:]}/logs/"
        res = run_process(self.command)[0].split('\t')

        return res[0]

    #--------------------
    def stack_trace(self) :
    #--------------------
        cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/pid/tc.pid'"
        pid,error = run_process(cf)
        self.command = f"{self.ssh_cmd()} jstack {pid}"
        res = run_process(self.command)

        return res

    
       


    #--------------------
    def tc_ctl(self,cmd) :
        #--------------------
        return f"'/opt/tomcat-home/sbin/{self.name.lower()}.sh {cmd}'"

    #--------------------
    def stop(self) :
        #--------------------
        self.command = f"{self.ssh_cmd()} {self.tc_ctl('stop')}"
        return run_process(self.command)
    #--------------------
    def start(self) :
        #--------------------
        self.command = f"{self.ssh_cmd()} {self.tc_ctl('start')}"
        return run_process(self.command)

    #--------------------
    def kill(self) :
        #--------------------
        user = "tcadminx"
        if self.env.name in ("PRD","DRC","PRD-02") :
            user = "tcadmin"
        self.command =  f"{self.ssh_cmd()} '/u/{user}/sbin/kill_tc.sh {self.name.lower()}'"
        return run_process(self.command)
    #--------------------
    def config_files(self,fname) :
        #--------------------
        safe = False
        m =  ""
        if fname == "setenv.sh" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/bin/setenv.sh'"
            message,error = run_process(cf)
            m = message.replace("\n","<br>")
            safe = True

        elif fname == "context.xml" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/conf/context.xml'"
            message,error = run_process(cf)
            mlist = message.split("\n")
            for mm in mlist :
                m += f'{escape(mm)}<br>'
            safe = True
        elif fname == "server.xml" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/conf/server.xml'"
            message,error = run_process(cf)
            # strip passwords
            mlist = message.split("\n")
            for mm in mlist :
                if "password" not in mm and "keystorepass" not in mm.lower() :
                    m += f'{escape(mm)}<br>'
                else :
                    m += "REDACTED PASSWORD<br>"
            safe = True
        elif fname == "uriworkermap.properties" :
            cf= f"{self.ssh_cmd()} 'cat /etc/httpd/conf/uriworkermap.properties'"
            message,error = run_process(cf)
            m = message.replace("\n","<br>")
            safe = True

        elif fname == "stack" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/pid/tc.pid'"
            pid,error = run_process(cf)
            self.command = f"{self.ssh_cmd()} jstack {pid}"
            message,error = run_process(cf)
            m = message.replace("\n","<br>")
            safe = True
        else:
            return "not Found",safe

        return m,safe



    #--------------------
    def raw_files(self,fname) :
        #--------------------
        m =  ""
        if fname == "setenv.sh" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/bin/setenv.sh'"
            message,error = run_process(cf)
            mlist = message.split("\n")
            for mm in mlist :
                if "password" in mm.lower() or "keystorepass"  in mm.lower() :
                    m += f"REDACTED PASSWORD\n"
                else :
                    m += f"{mm}\n"


        elif fname == "context.xml" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/conf/context.xml'"
            message,error = run_process(cf)
            m = message


        elif fname == "server.xml" :
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/conf/server.xml'"
            message,error = run_process(cf)
            # strip passwords
            mlist = message.split("\n")
            for mm in mlist :
                if "password" in mm.lower()  or "keystorepass"  in mm.lower() :
                    m += f"REDACTED PASSWORD\n"
                else :
                    m += f"{mm}\n"

        elif fname == "uriworkermap.properties" :
            cf= f"{self.ssh_cmd()} 'cat /etc/httpd/conf/uriworkermap.properties'"
            message,error = run_process(cf)
            m = message

        elif fname == "stack.txt" :
        
            cf= f"{self.ssh_cmd()} 'cat /opt/tomcat-base-{self.name[2:]}/pid/tc.pid'"
            pid,error = run_process(cf)
            self.command = f"{self.ssh_cmd()} jstack {pid}"
            message,error = run_process(self.command)
            m = message
 

        else:
            return "not Found"

        return m
#========================================
class App (models.Model) :
    #========================================
    name    =  models.CharField(max_length=128)
    env     =  models.ForeignKey(Env,on_delete=models.CASCADE)
    tc      =  models.ForeignKey(TC,on_delete=models.CASCADE)
    color   = models.CharField(max_length=30, default="inherit")
    status  = models.CharField(max_length=128, default="")

    #-----
    def start(self) :
        #-----
        return requests.get(f'{self.env.url}:{self.tc.port()}/manager/text/start?path=/{self.name}',auth=("deployer","tcmoda"))

    #-----
    def stop(self) :
        #-----
        return requests.get(f'{self.env.url}:{self.tc.port()}/manager/text/stop?path=/{self.name}',auth=("deployer","tcmoda"))



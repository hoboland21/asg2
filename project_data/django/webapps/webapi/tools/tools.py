import os,subprocess
import requests
from django.shortcuts import render
from webapi.models import *
from webapi.tcinfo import TCinfo
from .misc import *
from datetime import datetime

#----------------------
def init_db() :
#----------------------
    TC.objects.all().delete()
    Env.objects.all().delete()
    App.objects.all().delete()
    for env in ENVLIST :
        e = Env()
        applist=env_uriworker(env[0])
        e.name = env[0]
        e.server = env[1]
        e.authlvl = env[2]
        e.url=f"http://{e.server}.pdx.odshp.com"
        e.save()
        for tc in TCLIST :
            t = TC()
            t.name= tc
            t.env = e
            t.save()

            if tc in applist :
                for app in applist[tc] :
                    a = App()
                    a.name = app
                    a.env = e
                    a.tc = t
                    a.save()



#----------------------
def CMD_execute(act) :
#----------------------
    tcinfo = TCinfo()
    if act["action"] == "REFRESH" :
        tcinfo.refresh()
    if act["action"] == "TCREFRESH" :
        tc = TC.objects.get(id=int(act["id"]))
        tcinfo._refresh(tc)
        tcinfo.tc_refresh(tc)
    if act["action"] == "INITDB" :
        init_db()

    return act

#----------------------
def ActionReqApi(act) :
#----------------------
    if act["type"] == 'CMD' :
        return CMD_execute(act)
    elif act["type"] == 'App' :
        model = App.objects.get(id=int(act["id"]))
    elif act["type"] == 'TC' :
        model = TC.objects.get(id=int(act["id"]))
    elif act["type"] == 'Env' :
        model = Env.objects.get(id=int(act["id"]))
    else :
        act['error'] = 'Bad Type Submitted' 
        return act
    ex_array= {"START":model.start,"STOP":model.stop}
    if act["action"] in ex_array :
        try :
            act["result"] = ex_array[act["action"]]()
        except:
            act["error"] = "Exception"
    if act['type'] == "TC" and act['action'] == "KILL" :
        try:
            act["result"] = model.kill()
        except:
            act["error"] = "Exception"
    return act
               

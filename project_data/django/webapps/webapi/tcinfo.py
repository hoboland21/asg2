
# Create your views here.
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


from django.contrib.auth import logout

from .tools.misc import *
import os,subprocess
import requests
from .tools.api import *

from datetime import datetime

from .tools.ldap_tools import *
#========================================
class TCinfo(object) :
#========================================
  #-----
  def __init__(self) :
  #-----
    self.tclist = TC.objects.all()
    self.envlist = Env.objects.all()

  #-----
  def tc_refresh(self,tc) :
  #-----
    self.current_tc = tc
    self.current_apps = App.objects.filter(tc=tc).exclude(status="").order_by("name")



  #-----
  def Env_color_scan(self) :
  #-----
  ###DEVELOPMENT BYPASS
   # return
    for e in ENVLIST :
      env = Env.objects.get(name=e[0])
      if env.status()  :
        env.color='#CC3333' 
      else :
        env.color ='#99FF99'
      env.save()

  #-----
  def _refresh(self,tc) :
  #-----
  ###DEVELOPMENT BYPASS
   #   return
      tcs = tc.status()
      tc.color = "green"
      tc.save()
      if tcs != "ERROR" :
        for tt in tcs :
          t = tt.split(":")
          if len(t) == 4 and t[3] != 'ROOT' :
            try:
              app = App.objects.get(name=t[3],env=tc.env,tc=tc)
              app.status = t[1]
              if t[1] == "running":
                app.color = "green"
              elif t[1] == "stopped" :
                app.color = "yellow"
                tc.color = "yellow"
                tc.save() 
              else:
                app.color = "orange"
              app.save()
            except:
              pass
      else:
        tc.color = '#CC3333'
        tc.save()
        for app in App.objects.filter(env=tc.env,tc=tc) :
          app.color = "inherit"
          app.status = ""
          app.save()
 
  #-----
  def refresh(self) :
  #-----
  ###DEVELOPMENT BYPASS
  #  return
    self.Env_color_scan()
    for tc in self.tclist :
      self._refresh(tc)
  


  #-----
  def env_refresh(self,env) :
  #-----
    self.Env_color_scan()
    tclist = TC.objects.filter(env__name=env)
    for tc in tclist :
      self._refresh(tc)
  
  
  
  #-----
  def inactive_apps(self) :
  #-----
    return App.objects.all().exclude(status="running").exclude(status="")



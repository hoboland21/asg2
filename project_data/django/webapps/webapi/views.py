from django.shortcuts import render
# Create your views here.
import datetime
from rest_framework import serializers,status,viewsets,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.http import Http404
from django.contrib.auth.models import User, Group
import json 
from .tools.api import list_alerts, config_show
from .models import  Env,TC,App,Logs
from .serializer import  EnvSerializer,TCSerializer,AppSerializer,LogsSerializer
from .tools.tools import ActionReqApi, init_db
from .tools.ldap_tools import ldap_check


#-----------------------------------------------------
class LogsView(viewsets.ViewSet) :
#-----------------------------------------------------

  def create (self, request) :
    log = LogsSerializer(data=request.data)
    if log.is_valid() :
      log.save()
    return Response(request.data)

  def retrieve (self, request, count=None) :
    logs = Logs.objects.all().order_by('-id')[:int(count)]
    serializer = LogsSerializer(logs,many=True)
    return Response(serializer.data)

#-----------------------------------------------------
class Session(APIView) :
#-----------------------------------------------------
  def get (self, request,format=None) :
    ldap_check(request)
    res = request.session
    res.update({ 'user': request.user.username})

    return Response(res)

#-----------------------------------------------------
class Cmd(APIView) :
#-----------------------------------------------------
  def post (self, request,format=None) :
    return Response(ActionReqApi(request.data))
#-----------------------------------------------------
class EnvList(APIView) :
#-----------------------------------------------------
  def get (self, request, format=None) :
    env = Env.objects.all()
    serializer = EnvSerializer(env, many=True)
    return Response(serializer.data)
#-----------------------------------------------------
class GetEnv(APIView) :
#-----------------------------------------------------
  def get_object(self,pk):
    try:
      return Env.objects.get(pk=pk)
    except Env.DoesNotExist:
      raise Http404

  def get (self, request, envid, format=None) :
    env = self.get_object(int(envid))
    serializer = EnvSerializer(env)
    return Response(serializer.data)

#-----------------------------------------------------
class EnvStatus(APIView) :
#-----------------------------------------------------
  def get_object(self,envid):
    try:
      return Env.objects.get(id=envid)
    except Env.DoesNotExist:
      raise Http404

  def get (self,request,envid,format=None) :
    env = self.get_object(int(envid))
    return Response({"env_status":not env.status()})
#-----------------------------------------------------
class GetApps(APIView) :
#-----------------------------------------------------
  def get (self, request, tcid, format=None) :
    apps = App.objects.filter(tc__id=int(tcid)).order_by('name')
    serializer = AppSerializer(apps, many=True)
    return Response(serializer.data)

#-----------------------------------------------------
class TCList(APIView) :
#-----------------------------------------------------
  def get (self, request, envid, format=None) :
    tc = TC.objects.filter(env__id=envid).order_by('name')
    serializer = TCSerializer(tc, many=True)
    return Response(serializer.data)
#-----------------------------------------------------
class AppList(APIView) :
#-----------------------------------------------------
  def get (self, request, tcid, format=None) :
    app = App.objects.filter(tc=int(tcid)).order_by('name')
    serializer = AppSerializer(app, many=True)
    return Response(serializer.data)
#-----------------------------------------------------
class AppSearch(APIView) :
#-----------------------------------------------------
  def get (self, request, query, format=None) :
    app = App.objects.filter(env__name="PRD",name__icontains=query).order_by("name").values()
    for a in app :
      t = TC.objects.get(id=a['tc_id'])
      a['tcname'] = t.name
    return Response(app)

#-----------------------------------------------------
class NewRelic(APIView) :
#-----------------------------------------------------
  def get (self, request, format=None) :
        
    return Response(list_alerts())

#-----------------------------------------------------
class ConfigList(APIView) :
#-----------------------------------------------------
  def get (self, request, tcid, fname, format=None) :
        
    return Response({ "data" : config_show(tcid,fname)})

#-----------------------------------------------------
class StatusPage(APIView) :
#-----------------------------------------------------
  def get (self, request, tcid, format=None) :
    t = TC.objects.get(id=int(tcid))
    return Response({ "data" : t.tc_manager("status/all")})

#-----------------------------------------------------
class  StatusInfo(APIView) :
#-----------------------------------------------------
  def get(self,request,anyid,cmd,  formate=None) :
    result = {}
    if cmd == "tc_logsize" :
      t = TC.objects.get(id=int(anyid))
      result.update({"logsize":str(t.logsize())})
    if cmd == "env_logsize" :
      env = Env.objects.get(id=int(anyid))
      result.update({"logsize":env.logsize()})
    return Response(result)




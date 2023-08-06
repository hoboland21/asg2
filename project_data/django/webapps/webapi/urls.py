"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import TCList,EnvList,AppList,GetEnv,GetApps,Cmd,NewRelic,Session,AppSearch,ConfigList,StatusPage,EnvStatus,StatusInfo,LogsView

urlpatterns = [
    path('envstatus/<envid>/',EnvStatus.as_view()),
    path('envlist/',  EnvList.as_view()),
    path('env/<envid>/',  GetEnv.as_view()),
    path('app/<tcid>/',  GetApps.as_view()),
    path('cmd/',  Cmd.as_view()),
    path('tclist/<envid>/',  TCList.as_view()),
    path('newrelic/', NewRelic.as_view()),
    path('session/',Session.as_view()),
    path('appsearch/<query>/',AppSearch.as_view()),
    path('config/<tcid>/<fname>/',ConfigList.as_view()),
    path('status/<tcid>/',StatusPage.as_view()),
    path('postlog/',LogsView.as_view({'post':'create'})),
    path('listlogs/<count>/',LogsView.as_view({'get':'retrieve'})),
    path('info/<anyid>/<cmd>/',StatusInfo.as_view())
    ]

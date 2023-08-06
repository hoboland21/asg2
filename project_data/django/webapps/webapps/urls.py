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
#from tcadmin.views import main, logout
#from cmadmin.views import cmain
from django.contrib.auth import views as auth_views
from rest_framework import routers, serializers, viewsets,permissions
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken import views as tkn_views
import webapi


urlpatterns = [
    path('admin/',      admin.site.urls),
#    path('',            main,name="main"),
    path('webapi/',include('webapi.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/auth/', tkn_views.obtain_auth_token),
 #   path('api/ldap/',ldap.auth_profile.as_view(), name='auth_profile'),
 
#    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'),name="login"),
##    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'),name="logout"),
 #   path('accounts/profile/',  main,name="main"),
 #   path('cmadmin/', cmain, name="cmain"),

]


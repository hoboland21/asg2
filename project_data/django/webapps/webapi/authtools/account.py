
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from webapi.tools.ldap_tools import *
# ----------------------------
def user_synch(request,username,password) :
# ----------------------------
   user = authenticate(request, username=username, password=password)
   if user is not None:
      return 
   else:
      user = User.objects.create_user(username, '', password)
# ----------------------------
def ldap_check(request,username,password) :
# ----------------------------
   l = Ldap(username)
   if l.authorized_group() :
      if AD_Authenticate(username,password) :
         user_synch(request,username,password)
         return True
   return False
# ----------------------------
def login_view(request) :
# ----------------------------
   result = {}
   if 'username' in request.POST :
      if 'password' in request.POST :
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
            return redirect("main")

   '''      
         if ldap_check(request,username,password) :
            user = authenticate(request, username=username, password=password)
            if user is not None:
               login(request, user)
               return redirect("main")
   '''

   return render(request,'account/login.html',context=result)


# ----------------------------
def logout_view(request):
# ----------------------------
   result = {}   

   logout(request)
   
   return render(request,'account/logout.html',context=result)



from django.contrib.auth.models import User

from rest_framework import serializers
from .models import TC,App,Env,Logs

class EnvSerializer(serializers.ModelSerializer):
  class Meta:
    model= Env
    fields = ('__all__')

class TCSerializer(serializers.ModelSerializer):
  class Meta:
    model= TC
    fields = ('__all__')

class AppSerializer(serializers.ModelSerializer):
  class Meta:
    model= App
    fields = ('__all__')

class LogsSerializer(serializers.ModelSerializer):
  class Meta:
    model= Logs
    fields = ('__all__')


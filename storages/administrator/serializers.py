# Django
from django.contrib.auth import get_user_model

# Rest Framework
from rest_framework import serializers

# Customize
from storages.models import Storage
from users.employee.serializers import EmployeeSerializer

User = get_user_model()

class StorageSerializer(serializers.ModelSerializer):
    owner = EmployeeSerializer(read_only = True)
    class Meta:
        model = Storage
        fields = [ "id", "storage_name","length","width","height","owner" ]

class StorageRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = [ "id", "storage_name","length","width","height"]  

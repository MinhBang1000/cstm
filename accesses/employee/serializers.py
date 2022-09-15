# Django
from django.contrib.auth import get_user_model

# Rest framework
from rest_framework import serializers

# Customize
from accesses.models import Access
from storages.owner import serializers as storage_serializers
from storages.models import Storage
from users.employee import serializers as user_serializers

User = get_user_model()

class AccessSerializer(serializers.ModelSerializer):
    
    access_employee = user_serializers.EmployeeSerializer(read_only = True)
    access_storage = storage_serializers.StorageSerializer(read_only = True)

    class Meta:
        model = Access
        fields = [ 
            "id",
            "access_employee",
            "access_storage",
            "access_role",
            "access_from_owner",
            "access_accept"
        ]
        read_only_fields = [
            "access_role",
            "access_from_owner",
            "access_accept"
        ]

class AccessAcceptSerializer(serializers.ModelSerializer):

    access_employee = user_serializers.EmployeeSerializer(read_only = True)
    access_storage = storage_serializers.StorageSerializer(read_only = True)

    class Meta:
        model = Access
        fields = [ 
            "id",
            "access_employee",
            "access_storage",
            "access_role",
            "access_from_owner",
            "access_accept"
        ]
        read_only_fields = [ 
            "access_employee",
            "access_storage",
            "access_role",
            "access_from_owner"
        ]
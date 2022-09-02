# Django
from django.contrib.auth import get_user_model

# Rest Framework
from rest_framework import serializers

# Customize
from storages.models import Storage

User = get_user_model()

class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [ "id","email","first_name","last_name","role" ]
        read_only_fields = [ "id","email","first_name","last_name","role" ]

class StorageSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only = True)
    class Meta:
        model = Storage
        fields = [ "id", "storage_name","length","width","height","owner" ]
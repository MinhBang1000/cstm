# Rest framework
from rest_framework import serializers

# Customize
from storage_accesses.models import StorageAccess

class StorageAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorageAccess
        fields = [ "id","access_storage","access_employee" ]

class StorageAccessReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorageAccess
        fields = [ "id","access_storage" ]
        depth = 2
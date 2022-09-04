# Rest framework
from rest_framework import serializers

# Customize
from users.employee.serializers import EmployeeSerializer
from storages.administrator.serializers import StorageRelatedSerializer
from storage_invites.models import StorageEmployee


class StorageEmployeeSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only = True)
    storage = StorageRelatedSerializer(read_only = True)

    class Meta:
        model = StorageEmployee
        fields = [ "id","employee","storage","accepted","for_role","from_owner" ]
        read_only_fields = [ "id","accepted","from_owner" ]
    
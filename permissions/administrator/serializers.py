# Rest framework
from rest_framework import serializers

# Customize
from permissions.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [ "id","permission_name","permission_entity" ]
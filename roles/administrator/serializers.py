# Rest framework
from rest_framework import serializers

# Customize
from roles.models import Role
from permissions.administrator.serializers import PermissionReadSerializer, PermissionSerializer
from permissions.models import Permission

class RoleSerializer(serializers.ModelSerializer):
    role_permission_instances = PermissionReadSerializer(many=True, read_only=True, source="role_permissions")
    class Meta:
        model = Role 
        fields = [ "id", "role_name", "role_permissions", "role_permission_instances" ,"role_creater" ]
        read_only_fields = [ "role_creater" ]
        extra_kwargs = { 'role_permissions': {'write_only': True} }
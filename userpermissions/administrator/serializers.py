# Rest framework
from rest_framework import serializers

# Customize
from userpermissions.models import UserPermission
from permissions.administrator.serializers import PermissionSerializer
from users.employee.serializers import ProfileSerializer

class UserPermissionSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(read_only=True)
    person = ProfileSerializer(read_only=True)

    class Meta:
        model = UserPermission
        fields = [ "id","person","permission","is_active" ]
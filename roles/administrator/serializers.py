# Rest framework
from rest_framework import serializers

# Customize
from roles.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role 
        fields = [ "id", "role_name", "role_permissions","role_creater" ]
        read_only_fields = [ "role_creater" ]
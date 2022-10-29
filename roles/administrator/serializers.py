# Rest framework
from rest_framework import serializers

# Customize
from roles.models import Role

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role 
        fields = [ "id", "role_name" ]
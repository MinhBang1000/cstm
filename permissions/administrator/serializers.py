# Rest framework
from rest_framework import serializers

# Customize
from permissions.models import Permission
from missions.administrator.serializers import MissionSerializer

class PermissionSerializer(serializers.ModelSerializer):
    permission_mission = MissionSerializer()

    class Meta:
        model = Permission
        fields = [ "id","permission_name","permission_mission" ]
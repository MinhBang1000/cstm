# Rest framework
from rest_framework import serializers

# Customize
from missions.models import Mission

class MissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = [ "id", "mission_name" ]
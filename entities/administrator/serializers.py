# Rest framework
from rest_framework import serializers

# Customize
from entities.models import Entity

class EntitySerialzier(serializers.ModelSerializer):

    class Meta:
        model = Entity
        fields = [ "id","entity_name" ]

class EntityNameSerializer(serializers.ModelSerializer):
    entity_name = serializers.StringRelatedField()
    class Meta:
        model = Entity
        fields = ["entity_name"]
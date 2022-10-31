# Rest framework
from rest_framework import serializers

# Customize
from blocks.models import Block

class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block 
        fields = [ "id","block_permission", "block_user" ]
        extra_kwargs = {'block_user': {'write_only': True}}
# Rest framework
from rest_framework import serializers

# Customize
from locations.models import Location

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = [ "id","location_x","location_y","location_z","location_pallet" ]
        extra_kwargs = { "location_pallet": { "read_only": True } }
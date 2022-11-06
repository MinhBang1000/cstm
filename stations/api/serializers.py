# Rest framework
from rest_framework import serializers

# Customize
from stations.models import Station
from storages.models import Storage

class StationSerializer(serializers.ModelSerializer):
    station_storage_id = serializers.PrimaryKeyRelatedField(
        queryset = Storage.objects.all(),
        write_only = True,
        source = "station_storage"
    )

    class Meta:
        model = Station
        fields = [ "id","station_username","station_password","station_storage","station_storage_id" ]
        extra_kwargs = { 'station_storage': { 'read_only': True } }
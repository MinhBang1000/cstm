# Rest framework
from rest_framework import serializers

# Customize
from sensors.models import Sensor
from storages.owner import serializers as storage_serializers
from storages.models import Storage

class SensorSerializer(serializers.ModelSerializer):
    
    # sensor_storage = storage_serializers.StorageSerializer(read_only = True)
    sensor_storage_id = serializers.PrimaryKeyRelatedField(
        queryset = Storage.objects.all(),
        write_only = True,
        source = "sensor_storage"
    )

    class Meta:
        model = Sensor
        fields = [ "id", "sensor_x", "sensor_y", "sensor_z",  "sensor_storage_id" ]
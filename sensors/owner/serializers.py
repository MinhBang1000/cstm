# Rest framework
from rest_framework import serializers

# Customize
from sensors.models import Sensor
from storages.models import Storage

class SensorSerializer(serializers.ModelSerializer):
    
    sensor_storage_id = serializers.PrimaryKeyRelatedField(
        queryset = Storage.objects.all(),
        write_only = True,
        source = "sensor_storage"
    )

    class Meta:
        model = Sensor
        fields = [ "id", "sensor_x", "sensor_y", "sensor_z", "sensor_temperature", "sensor_storage_id" ]
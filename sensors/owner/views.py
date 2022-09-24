# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, permission_classes

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from sensors.models import Sensor
from sensors.owner import serializers as sensor_serializers
from storages.models import Storage


class SensorViewSet(BaseViewSet):
    serializer_class = sensor_serializers.SensorSerializer
    permission_classes = [base_permissions.IsOwnerAdmin]
    filterset_fields = [ "sensor_x", "sensor_y", "sensor_z", "sensor_storage__storage_name", "sensor_storage__storage_code", "sensor_storage__id" ]
    
    def get_queryset(self):
        return Sensor.objects.filter(sensor_storage__storage_branch__branch_company__company_owner = self.request.user)

    def perform_create(self, serializer):
        x = self.request.data["sensor_x"]
        y = self.request.data["sensor_y"]
        z = self.request.data["sensor_z"]
        sensor = Sensor.objects.filter(sensor_x = x, sensor_y = y, sensor_z = z, sensor_storage = self.request.data["sensor_storage_id"])
        if len(sensor) != 0:
            raise ValidationError(errors.get_error(errors.SENSOR_EXISTS))
        try:
            storage = Storage.objects.get(pk = self.request.data["sensor_storage_id"])
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        if storage.storage_branch.branch_company.company_owner != self.request.user:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        if self.request.data.get("sensor_storage_id", False) != False:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_STORAGE_OF_SENSOR))
        try:
            sensor = Sensor.objects.get(pk = self.kwargs.get("pk", False))
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_SENSOR)) 
        x = self.request.data.get("sensor_x", False) if self.request.data.get("sensor_x", False) != False else sensor.sensor_x 
        y = self.request.data.get("sensor_y", False) if self.request.data.get("sensor_y", False) != False else sensor.sensor_y
        z = self.request.data.get("sensor_z", False) if self.request.data.get("sensor_z", False) != False else sensor.sensor_z
        sensor = Sensor.objects.filter(sensor_x = x, sensor_y = y, sensor_z = z, sensor_storage = sensor.sensor_storage.id)
        if len(sensor) != 0:
            raise ValidationError(errors.get_error(errors.SENSOR_EXISTS))
        return super().perform_update(serializer)
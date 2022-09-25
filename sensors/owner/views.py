# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, permission_classes

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from bases import trilinear_interpolation as trilinear
from sensors.models import Sensor
from sensors.owner import serializers as sensor_serializers
from storages.models import Storage


class SensorViewSet(BaseViewSet):
    serializer_class = sensor_serializers.SensorSerializer
    permission_classes = [base_permissions.IsOwnerAdmin]
    filterset_fields = [ "sensor_x", "sensor_y", "sensor_z", "sensor_storage__storage_name", "sensor_storage__storage_code", "sensor_storage__id" ]
    
    def get_queryset(self):
        return Sensor.objects.filter(sensor_storage__storage_branch__branch_company__company_owner = self.request.user)

    def has_enough_primary_sensor(self, storage_id):
        sensors = Sensor.objects.filter(sensor_storage = storage_id)
        # Check not found storage in previous function
        storage = Storage.objects.get(pk = storage_id)
        count = 0
        for sensor in sensors:
            if sensor.sensor_x in [ storage.storage_length, 0 ] and sensor.sensor_y in [ storage.storage_width, 0 ] and sensor.sensor_z in [ storage.storage_height, 0 ]:
                count += 1
        return count == 8
    
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
        super().perform_create(serializer)
        # Caculating total space when we have enough primary sensors
        if self.has_enough_primary_sensor(self.request.data["sensor_storage_id"]) == True:
            # Init whole storage space
            storage_space = {
                "x_min": 0,
                "y_min": 0,
                "z_min": 0,
                "x_max": storage.storage_length,
                "y_max": storage.storage_width,
                "z_max": storage.storage_height
            }
            # Init variable was needing
            list_of_sensor = Sensor.objects.filter(sensor_storage = self.request.data["sensor_storage_id"])
            template_sensors = []
            for sensor in list_of_sensor:
                template_sensors.append({
                    "location": {
                        "x":sensor.sensor_x,
                        "y":sensor.sensor_y,
                        "z":sensor.sensor_z
                    },
                    "temperature": 0
                })
            trilinear.secondary_sensors = trilinear.divide_sensor_list(storage_space, template_sensors)["secondary_sensors"]
            trilinear.mark_of_secondary_sensors = [  False for i in trilinear.secondary_sensors  ]
            # Caculate by above variable
            trilinear.generate_total_spaces(storage_space)

    def perform_update(self, serializer):
        if self.request.data.get("sensor_storage_id", False) != False:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_STORAGE_OF_SENSOR))
        try:
            sensor = Sensor.objects.get(pk = self.kwargs.get("pk", False))
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_SENSOR)) 
        x = self.request.data.get("sensor_x", None) if self.request.data.get("sensor_x", None) != None else sensor.sensor_x 
        y = self.request.data.get("sensor_y", None) if self.request.data.get("sensor_y", None) != None else sensor.sensor_y
        z = self.request.data.get("sensor_z", None) if self.request.data.get("sensor_z", None) != None else sensor.sensor_z
        sensors = Sensor.objects.filter(sensor_x = x, sensor_y = y, sensor_z = z, sensor_storage = sensor.sensor_storage.id)
        if len(sensors) != 0:
            raise ValidationError(errors.get_error(errors.SENSOR_EXISTS))
        return super().perform_update(serializer)
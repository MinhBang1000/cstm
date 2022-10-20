# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, permission_classes

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from sensors.models import Sensor
from sensors.owner import serializers as sensor_serializers
from storages.models import Storage
from bases.solving_code.SpaceSaver import SpaceSaver
from bases.solving_code.Space import Space as SpaceClass
from bases.solving_code.Storage import Storage as StorageClass 
from bases.solving_code.Sensor import Sensor as SensorClass
from bases.solving_code.SpaceDividing import SpaceDividing as SpaceDividingClass


class SensorViewSet(BaseViewSet):
    serializer_class = sensor_serializers.SensorSerializer
    permission_classes = [base_permissions.IsOwnerAdmin]
    filterset_fields = [ "sensor_x", "sensor_y", "sensor_z", "sensor_storage__storage_name", "sensor_storage__storage_code", "sensor_storage__id" ]
    
    def get_queryset(self):
        return Sensor.objects.filter(sensor_storage__storage_branch__branch_company__company_owner = self.request.user)

    def has_enough_primary_sensor(self, storage):
        sensors = Sensor.objects.filter(sensor_storage = storage.id)
        # Check not found storage in previous function
        count = 0
        for sensor in sensors:
            if sensor.sensor_x in [ storage.storage_length, 0 ] and sensor.sensor_y in [ storage.storage_width, 0 ] and sensor.sensor_z in [ storage.storage_height, 0 ]:
                count += 1
        return count == 8

    def caculating_total_spaces(self, storage):
        if self.has_enough_primary_sensor(storage) == True:
            # Init whole storage space
            storage_obj = StorageClass(storage)
            storage_space = SpaceClass(0,0,0,storage_obj.x_max,storage_obj.y_max,storage_obj.z_max)
            print("Storage space:")
            print(storage_space.get_space())
            # Init variable was needing
            sensors = []
            sensor_instances = Sensor.objects.filter(sensor_storage = storage.id)
            for s_item in sensor_instances:
                sensor = SensorClass(s_item)
                print(sensor.get_sensor())
                sensors.append(sensor)
            smaller_spaces = SpaceDividingClass(storage_space) 
            # To avoid use again any part previously
            smaller_spaces.reset_for_sure()  
            smaller_spaces.generate_secondary_sensors(sensors)
            smaller_spaces.generate_mark_secondary_sensors()
            smaller_spaces.generate_total_spaces()
            saver = SpaceSaver()
            saver_spaces = [ space.get_space() for space in smaller_spaces.spaces ]
            saver.local_write(saver_spaces, storage.id)

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
        # Create a new instance for sensor
        super().perform_create(serializer)
        # Caculating total space when we have enough primary sensors
        self.caculating_total_spaces(storage)

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
        flag = True 
        if self.request.data.get("sensor_x", None) == None and self.request.data.get("sensor_y", None) == None and self.request.data.get("sensor_z", None) == None:
            flag = False 
        sensors = Sensor.objects.filter(sensor_x = x, sensor_y = y, sensor_z = z, sensor_storage = sensor.sensor_storage.id)
        if flag == True and len(sensors) != 0:
            raise ValidationError(errors.get_error(errors.SENSOR_EXISTS))
        # Update the sensor
        super().perform_update(serializer)
        # Caculating total spaces after we have had enough primary sensors
        self.caculating_total_spaces(sensor.sensor_storage)
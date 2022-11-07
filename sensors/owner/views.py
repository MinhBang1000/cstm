# Python 
import requests

# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

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
from branch_accesses.models import BranchAccess
from storage_accesses.models import StorageAccess
from stations.models import Station

class SensorViewSet(BaseViewSet):
    serializer_class = sensor_serializers.SensorSerializer
    permission_classes = [ permissions.IsAuthenticated ]
    filterset_fields = [ "sensor_x", "sensor_y", "sensor_z", "sensor_storage__storage_name", "sensor_storage__storage_code", "sensor_storage__id" ]
    view_name = "sensor"

    def get_queryset(self):
        if self.is_owner() == True:
            return Sensor.objects.filter( sensor_storage__storage_branch__branch_company__company_owner = self.request.user )
        access = None
        try:
            access = StorageAccess.objects.get( access_employee = self.request.user )
        except:
            pass
        if access == None:
            try:
                access = BranchAccess.objects.get( access_employee = self.request.user )
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
            return Sensor.objects.filter( sensor_storage__storage_branch = access.access_branch )
        return Sensor.objects.filter( sensor_storage = access.access_storage )

    def check_permissions(self, request):
        # To check user permissions - do not review block permissions yet
        self_check = self.is_permission(self.view_name)
        if self_check == False:
            raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))        
        return super().check_permissions(request)
    
    def has_enough_primary_sensor(self, storage):
        sensors = Sensor.objects.filter(sensor_storage = storage.id)
        # Check not found storage in previous function
        count = 0
        for sensor in sensors:
            if sensor.sensor_x in [ storage.storage_length, 0 ] and sensor.sensor_y in [ storage.storage_width, 0 ] and sensor.sensor_z in [ storage.storage_height, 0 ]:
                count += 1
        return count == 8

    def call_external_api(self):
        username = 'tester@kholanhctu'
        password = 'tester@123'
        url = 'https://fake-sensors.herokuapp.com/sensors/'
        r = requests.get(url=url, auth=(username, password))
        r_status_code = r.status_code
        if r_status_code == 200:
            pass
        else:
            print(r_status_code)
    
    # requests.post('https://httpbin.org/post', data={'key':'value'})
    def create_sensor_iot_lab(self, username, password, data):
        url = 'https://fake-sensors.herokuapp.com/sensors/'
        r = requests.post(url, data, auth=(username, password))
        if r.status_code != 201:
            raise ValidationError(errors.get_error(errors.CAN_NOT_PERFORM))
        return r.json()

    # requests.delete('https://httpbin.org/delete')
    def delete_sensor_iot_lab(self, id, username, password):
        url = 'https://fake-sensors.herokuapp.com/sensors/'+str(id)+"/"
        r = requests.delete(url, auth=(username, password))
        print(r.status_code)
        if r.status_code != 204:
            raise ValidationError(errors.get_error(errors.CAN_NOT_PERFORM))

    # requests.put('https://httpbin.org/put', data={'key':'value'})
    def update_sensor_iot_lab(self, id, username, password, data):
        url = 'https://fake-sensors.herokuapp.com/sensors/'+str(id)+"/"
        r = requests.put(url, data, auth=(username, password))
        if r.status_code != 200:
            raise ValidationError(errors.get_error(errors.CAN_NOT_PERFORM))
        return r.json()

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
        # Check owner or employee
        access = None
        if self.is_owner() == True:
            if storage.storage_branch.branch_company.company_owner != self.request.user:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = self.request.user, access_branch = storage.storage_branch ).first()
                except:
                    pass
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        # Create a new instance for sensor in IOT LAB API
        try:
            station = Station.objects.filter( station_storage = storage ).first()
        except:
            pass 
        if station == None:
            raise ValidationError(errors.get_error(errors.AUTHENICATION_IN_IOT))
        # Create a new instance for sensor
        instance = serializer.save()        
        iot_data = {
            "x": instance.sensor_x,
            "y": instance.sensor_y,
            "z": instance.sensor_z,
            "temperature": instance.sensor_temperature,
            "identify": instance.id
        }
        response_json = self.create_sensor_iot_lab(station.station_username, station.station_password, iot_data)
        instance.sensor_code = response_json["id"]
        instance.save()
        # Caculating total space when we have enough primary sensors
        self.caculating_total_spaces(storage)

    def perform_update(self, serializer):
        if self.request.data.get("sensor_storage_id", False) != False:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_STORAGE_OF_SENSOR))
        try:
            sensor = Sensor.objects.get(pk = self.kwargs.get("pk", False))
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_SENSOR)) 
        storage = sensor.sensor_storage
        # Check owner or employee
        access = None
        if self.is_owner() == True:
            if storage.storage_branch.branch_company.company_owner != self.request.user:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = self.request.user, access_branch = storage.storage_branch ).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        x = self.request.data.get("sensor_x", None) if self.request.data.get("sensor_x", None) != None else sensor.sensor_x 
        y = self.request.data.get("sensor_y", None) if self.request.data.get("sensor_y", None) != None else sensor.sensor_y
        z = self.request.data.get("sensor_z", None) if self.request.data.get("sensor_z", None) != None else sensor.sensor_z
        flag = True 
        if self.request.data.get("sensor_x", None) == None and self.request.data.get("sensor_y", None) == None and self.request.data.get("sensor_z", None) == None:
            flag = False 
        sensors = Sensor.objects.filter(sensor_x = x, sensor_y = y, sensor_z = z, sensor_storage = sensor.sensor_storage.id)
        if flag == True and len(sensors) != 0:
            raise ValidationError(errors.get_error(errors.SENSOR_EXISTS))
        # Create a new instance for sensor in IOT LAB API
        try:
            station = Station.objects.filter( station_storage = storage ).first()
        except:
            pass 
        if station == None:
            raise ValidationError(errors.get_error(errors.AUTHENICATION_IN_IOT))
        # Update the sensor
        instance = serializer.save()
        iot_data = {
            "x": instance.sensor_x,
            "y": instance.sensor_y,
            "z": instance.sensor_z,
            "temperature": instance.sensor_temperature,
            "identify": instance.id
        }
        response_json = self.update_sensor_iot_lab(instance.sensor_code, station.station_username, station.station_password, iot_data)
        # Caculating total spaces after we have had enough primary sensors
        self.caculating_total_spaces(sensor.sensor_storage)

    def perform_destroy(self, instance):
        try:
            sensor = Sensor.objects.get(pk = self.kwargs.get("pk", False))
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_SENSOR)) 
        storage = sensor.sensor_storage
        # Check owner or employee
        access = None
        if self.is_owner() == True:
            if storage.storage_branch.branch_company.company_owner != self.request.user:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = self.request.user, access_branch = storage.storage_branch ).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        # Delete a instance for sensor in IOT LAB API
        try:
            station = Station.objects.filter( station_storage = storage ).first()
        except:
            pass 
        if station == None:
            raise ValidationError(errors.get_error(errors.AUTHENICATION_IN_IOT))
        self.delete_sensor_iot_lab(sensor.sensor_code, station.station_username, station.station_password)
        # To delete
        super().perform_destroy(instance)
        # Caculating total spaces after we have had enough primary sensors
        self.caculating_total_spaces(storage)
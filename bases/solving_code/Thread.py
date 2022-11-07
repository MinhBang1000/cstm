# Python
from threading import Thread
import time
import requests
from .StartThread import check_real_time_update
import os

# Customize
from sensors.models import Sensor
from stations.models import Station
from sensors.owner.serializers import SensorSerializer
from bases.solving_code.SpaceSaver import SpaceSaver
from bases.solving_code.Space import Space as SpaceClass
from bases.solving_code.Storage import Storage as StorageClass 
from bases.solving_code.SpaceDividing import SpaceDividing as SpaceDividingClass
from bases.solving_code.Sensor import Sensor as SensorClass
class SensorThread(Thread):
    def __init__(self, delay):
        super(SensorThread, self).__init__() 
        self.delay = delay

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

    def call_list_sensors(self):
        url = 'https://fake-sensors.herokuapp.com/sensors/'
        # Admin of IOT LAB for update all sensors temperatures
        response = requests.get(url, auth=(os.getenv("IOT_USERNAME"), os.getenv("IOT_PASSWORD")))
        print(response.json(), os.getenv("IOT_USERNAME"))
        data = response.json()
        # Find all stations we have
        try:
            stations = Station.objects.all()
        except:
            pass 
        # Delete all sensors for add new sensors
        try:
            sensors = Sensor.objects.all()
        except:
            pass 
        for sensor in sensors:
            sensor.delete()
        # Create group of sensors for station
        for station in stations:
            for item in data:
                if station.station_username == item["owner"]["username"]:
                    input_data = {
                        "sensor_x": item["x"],
                        "sensor_y": item["y"],
                        "sensor_z": item["z"],
                        "sensor_temperature": item["temperature"],
                        "sensor_storage_id": station.station_storage.id
                    }
                    serializer = SensorSerializer(data = input_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(sensor_code = item["id"])
            # Recalculate about storage space 
            self.caculating_total_spaces(station.station_storage)
                    
    def run(self) -> None:
        count = 0
        while check_real_time_update()==True:
            # Noice
            count += 1
            print("Updating for", count, "times")
            # Do anything in here
            self.call_list_sensors()
            # Timer 
            time.sleep(self.delay)
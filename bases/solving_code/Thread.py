# Python
from threading import Thread
import time
import requests
from .StartThread import check_real_time_update
import os

# Customize
from sensors.models import Sensor

class SensorThread(Thread):
    def __init__(self, delay):
        super(SensorThread, self).__init__() 
        self.delay = delay

    def call_list_sensors(self):
        url = 'https://fake-sensors.herokuapp.com/sensors/'
        # Admin of IOT LAB for update all sensors temperatures
        response = requests.get(url, auth=(os.getenv("IOT_USERNAME"), os.getenv("IOT_PASSWORD")))
        print(response.json(), os.getenv("IOT_USERNAME"))
        data = response.json()
        # Add to database
        try:
            sensors = Sensor.objects.all()
        except:
            pass 
        flag = True
        for dt in data:
            flag = True
            for sensor in sensors:
                if sensor.sensor_code == dt["id"] and flag == True:
                    sensor.sensor_temperature = dt["temperature"]
                    sensor.save()
                    flag = False 
                    
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
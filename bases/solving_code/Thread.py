# Python
from threading import Thread
import time
import requests

# Customize
from sensors.models import Sensor

class SensorThread(Thread):
    station = None

    def __init__(self, counter, delay, station):
        super(SensorThread, self).__init__() 
        self.counter = counter
        self.delay = delay
        self.station = station

    def set_station(self, station):
        self.storage = station

    def call_list_sensors(self):
        url = 'https://fake-sensors.herokuapp.com/sensors/'
        response = requests.get(url, auth=(self.station.station_username, self.station.station_password))
        print(response.json())
        data = response.json()
        # Add to database
        try:
            sensors = Sensor.objects.filter( sensor_storage = self.station.station_storage )
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
        while self.counter!=0:
            # Noice
            print(self.counter," second")
            # Do anything in here
            self.call_list_sensors()
            # Timer 
            time.sleep(self.delay)
            self.counter = self.counter - 1
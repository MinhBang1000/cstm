# Django
from django.db import models

# Customize
from storages.models import Storage

class Sensor(models.Model):
    sensor_x = models.IntegerField()
    sensor_y = models.IntegerField()
    sensor_z = models.IntegerField()
    sensor_storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="sensors")


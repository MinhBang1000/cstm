from django.db import models
from storages.models import Storage

# Create your models here.
class Station(models.Model):
    station_username = models.CharField(max_length = 250)
    station_password = models.CharField(max_length = 250)
    station_storage = models.ForeignKey(Storage, on_delete = models.CASCADE, related_name = "storage_stations")

    def __str__(self) -> str:
        return self.station_username+"_Kho lanh "+str(self.station_storage.id)
# Django
from django.db import models
from django.contrib.auth import get_user_model

# Customize
from storages.models import Storage

User = get_user_model()

class Area(models.Model):
    x_min = models.IntegerField()
    y_min = models.IntegerField()
    z_min = models.IntegerField()
    x_max = models.IntegerField()
    y_max = models.IntegerField()
    z_max = models.IntegerField()
    monitor_from = models.IntegerField()
    monitor_to = models.IntegerField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    status = models.BooleanField(default=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="areas")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="areas")
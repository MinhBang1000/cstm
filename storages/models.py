from django.db import models
from django.contrib.auth import get_user_model

class Storage(models.Model):
    storage_name = models.CharField(max_length=250)
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    storage_code = models.CharField(max_length=64, default=None)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="owner_storages")
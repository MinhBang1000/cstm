from django.db import models
from django.contrib.auth import get_user_model

class Storage(models.Model):
    storage_name = models.CharField(max_length=250)
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="owner_storages")

class StorageEmployee(models.Model):
    employee = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=False, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    accepted = models.BooleanField(default=False)

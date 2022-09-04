# Django 
from django.contrib.auth import get_user_model
from django.db import models

# Customize
from storages.models import Storage

class StorageEmployee(models.Model):
    employee = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=False, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    for_role = models.CharField(max_length=50, default="Supervisor", blank=True, null=True)
    accepted = models.BooleanField(default=False)
    from_owner = models.BooleanField(default=True)
    # Owner invite when from_owner = True
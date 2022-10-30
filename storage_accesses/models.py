from django.db import models
from django.contrib.auth import get_user_model
from storages.models import Storage
User = get_user_model()

# Create your models here.
class StorageAccess(models.Model):
    access_storage = models.ForeignKey(Storage, on_delete = models.CASCADE, related_name = "storage_accesses")
    access_employee = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = False, related_name = "storage_employee_access")
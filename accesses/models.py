# Django
from django.db import models
from django.contrib.auth import get_user_model

# Customize
from storages.models import Storage

User = get_user_model()

class Access(models.Model):
    access_employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_accesses")
    access_storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="storage_accesses")
    access_role = models.CharField(max_length=50, default="Supervisor")
    access_from_owner = models.BooleanField(default=False)
    access_accept = models.BooleanField(default=False)
    access_created = models.DateTimeField(auto_now_add=True)
    access_updated = models.DateTimeField(auto_now=True)

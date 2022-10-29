# Django
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Customize
from districts.models import District
from branches.models import Branch

class Storage(models.Model):
    storage_name = models.CharField(max_length=250)
    storage_length = models.IntegerField()
    storage_width = models.IntegerField()
    storage_height = models.IntegerField()
    storage_code = models.CharField(max_length=64, default=None)
    storage_street = models.CharField(max_length=250)
    storage_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="district_storages")
    storage_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branch_storages")
    storage_manager = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, primary_key = False, related_name="manager_storage")
    storage_created = models.DateTimeField(auto_now_add=True)
    storage_updated = models.DateTimeField(auto_now=True)
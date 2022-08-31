from django.contrib import admin
from storages.models import Storage, StorageEmployee

# Register your models here.
admin.site.register([StorageEmployee, Storage])
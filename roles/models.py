from django.db import models
from permissions.models import Permission
# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=250)
    role_permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self) -> str:
        return self.role_name
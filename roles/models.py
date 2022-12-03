from email.policy import default
from django.db import models
from permissions.models import Permission
# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=250)
    role_permissions = models.ManyToManyField(Permission, blank=True)
    role_creater = models.IntegerField(default = 0)
    role_level = models.IntegerField(default = 3)

    def __str__(self) -> str:
        return self.role_name
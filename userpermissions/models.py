from django.db import models
from permissions.models import Permission
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class UserPermission(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permission_persons")
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.person.email +"/"+self.permission.permission_name+"-"+self.permission.permission_mission.mission_name
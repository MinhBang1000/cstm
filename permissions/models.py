from django.db import models
from missions.models import Mission

# Create your models here.
class Permission(models.Model):
    permission_name = models.CharField(max_length = 250)
    permission_mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="mission_permissions")
    
    def __str__(self) -> str:
        return self.permission_name + "-" + self.permission_mission.mission_name
from django.db import models
from entities.models import Entity
# Create your models here.
class Permission(models.Model):
    permission_name = models.CharField(max_length = 250)
    permission_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name = "entity_permissions")
    permission_level = models.IntegerField(default = 3)

    def __str__(self) -> str:
        return self.permission_name + "_" + self.permission_entity.entity_name +"_"+ str(self.permission_level)
    
    def get_str(self)->str:
        return self.permission_name + "_" + self.permission_entity.entity_name
from django.db import models

# Create your models here.
class Entity(models.Model):
    entity_name = models.CharField(max_length = 250)

    def __str__(self) -> str:
        return self.entity_name
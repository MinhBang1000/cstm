from django.db import models

# Create your models here.
class Mission(models.Model):
    mission_name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.mission_name
# Django
from django.db import models

# Customize
from provinces.models import Province

class District(models.Model):
    district_name = models.CharField(max_length=250)
    district_province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="districts")

    def __str__(self) -> str:
        return self.district_name
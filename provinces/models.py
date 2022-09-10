from django.db import models

class Province(models.Model):
    province_name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.province_name
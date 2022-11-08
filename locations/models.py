from django.db import models
from django.core.validators import MinValueValidator
from pallets.models import Pallet 
# Create your models here.

class Location(models.Model):
    location_x = models.IntegerField(validators = [MinValueValidator(0)])
    location_y = models.IntegerField(validators = [MinValueValidator(0)])
    location_z = models.IntegerField(validators = [MinValueValidator(0)])
    location_pallet = models.ForeignKey(Pallet,on_delete = models.CASCADE, related_name = "pallet_locations")
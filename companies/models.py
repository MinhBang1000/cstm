# Django
from django.db import models
from django.contrib.auth import get_user_model

# Customize
from districts.models import District

User = get_user_model()

class Company(models.Model):
    company_name = models.CharField(max_length=250)
    company_street = models.CharField(max_length=250)
    company_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="district_companies")
    company_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_companies")
    company_created = models.DateTimeField(auto_now_add=True)
    company_updated = models.DateTimeField(auto_now=True)
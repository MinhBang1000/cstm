# Django
from django.db import models

# Customize
from districts.models import District
from companies.models import Company

class Branch(models.Model):
    branch_name = models.CharField(max_length=250)
    branch_street = models.CharField(max_length=250)
    branch_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="district_branches")
    branch_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_branches")
    branch_created = models.DateTimeField(auto_now_add=True)
    branch_updated = models.DateTimeField(auto_now=True)

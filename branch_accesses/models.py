from django.db import models
from django.contrib.auth import get_user_model
from branches.models import Branch
User = get_user_model()

# Create your models here.
class BranchAccess(models.Model):
    access_branch = models.ForeignKey(Branch, on_delete = models.CASCADE, related_name = "branch_accesses")
    access_employee = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = False, related_name = "branch_employee_access")

    def __str__(self) -> str:
        return self.access_branch.branch_company.company_name +"_"+self.access_branch.branch_name+"_"+self.access_employee.email
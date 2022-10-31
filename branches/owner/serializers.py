# Rest framework
from rest_framework import serializers

# Customize
from branches.models import Branch
from districts.models import District
from companies.models import Company
from districts.administrator import serializers as district_serializer
from companies.owner import serializers as company_serializer
from users.employee import serializers as employee_serializers

class BranchSerializer(serializers.ModelSerializer):

    branch_district_id = serializers.PrimaryKeyRelatedField(
        queryset = District.objects.all(),
        source = "branch_district",
        write_only = True
    )    
    branch_company_id = serializers.PrimaryKeyRelatedField(
        queryset = Company.objects.all(),
        write_only = True,
        source = "branch_company"
    )
    branch_district = district_serializer.DistrictSerializer(read_only = True)
    branch_company = company_serializer.CompanySerializer(read_only = True)
    class Meta:
        model = Branch
        fields = [ "id","branch_name","branch_street","branch_district","branch_district_id","branch_company","branch_company_id" ]
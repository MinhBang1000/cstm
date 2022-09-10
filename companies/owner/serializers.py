# Rest framework
from rest_framework import serializers

# Customize
from companies.models import Company
from districts.administrator import serializers as district_serializer
from districts.models import District
from users.employee import serializers as employee_serializer

class CompanySerializer(serializers.ModelSerializer):

    company_district = district_serializer.DistrictSerializer(read_only = True)
    company_district_id = serializers.PrimaryKeyRelatedField(
        write_only = True,
        queryset = District.objects.all(),
        source = "company_district"
    )
    company_owner = employee_serializer.EmployeeSerializer(read_only = True)

    class Meta:
        model = Company
        fields = [ "id", "company_name", "company_street", "company_district", "company_district_id", "company_owner", "company_created", "company_updated" ]
# Rest framework
from rest_framework import serializers

# Customize
from provinces.administrator import serializers as province_serializer
from districts.models import District
from provinces.models import Province

class DistrictSerializer(serializers.ModelSerializer):

    district_province = province_serializer.ProvinceSerializer(read_only = True)
    district_province_id = serializers.PrimaryKeyRelatedField(
        write_only = True,
        source = "district_province",
        queryset = Province.objects.all()
    )

    class Meta:
        model = District
        fields = [ "id","district_name","district_province","district_province_id" ]
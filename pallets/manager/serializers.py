# Rest framework
from rest_framework import serializers

# Customize
from pallets.models import Pallet
from storages.models import Storage
from locations.api.serializers import LocationSerializer

class PalletSerializer(serializers.ModelSerializer):

    pallet_storage_id = serializers.PrimaryKeyRelatedField(
        queryset = Storage.objects.all(),
        write_only = True,
        source = "pallet_storage"
    )
    pallet_locations = LocationSerializer(many = True, read_only = True)

    class Meta:
        model = Pallet 
        fields = [ 
            "id",
            "pallet_length",
            "pallet_width",
            "pallet_height",
            "pallet_drawers",
            "pallet_active",
            "pallet_color",
            "pallet_storage_id",
            "pallet_locations"
        ]
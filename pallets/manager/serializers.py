# Rest framework
from rest_framework import serializers

# Customize
from pallets.models import Pallet
from storages.models import Storage

class PalletSerializer(serializers.ModelSerializer):

    pallet_storage_id = serializers.PrimaryKeyRelatedField(
        queryset = Storage.objects.all(),
        write_only = True,
        source = "pallet_storage"
    )

    class Meta:
        model = Pallet 
        fields = [ "id","pallet_x","pallet_y","pallet_y","pallet_length","pallet_width","pallet_height","pallet_drawers","pallet_storage_id" ]
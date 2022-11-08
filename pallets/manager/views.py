# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from pallets.manager import serializers as pallet_serializers
from pallets.models import Pallet
from branch_accesses.models import BranchAccess
from storage_accesses.models import StorageAccess
from storages.models import Storage
from locations.models import Location
from locations.api import serializers as location_serializers

class PalletViewSet(BaseViewSet):
    serializer_class = pallet_serializers.PalletSerializer
    permission_classes = [ permissions.IsAuthenticated ]
    filterset_fields = [ "id","pallet_length","pallet_width","pallet_height","pallet_color","pallet_drawers","pallet_storage__id" ]
    view_name = "pallet"

    def get_queryset(self):
        if self.is_owner() == True:
            return Pallet.objects.filter( pallet_storage__storage_branch__branch_company__company_owner = self.request.user )
        access = None
        try:
            access = StorageAccess.objects.filter( access_employee = self.request.user ).first()
        except:
            pass 
        if access == None:
            try:
                access = BranchAccess.objects.filter(access_employee = self.request.user ).first()
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
            return Pallet.objects.filter( pallet_storage__storage_branch = access.access_branch )
        return Pallet.objects.filter( pallet_storage = access.access_storage )

    def check_permissions(self, request):
        # To check user permissions - do not review block permissions yet
        self_check = self.is_permission(self.view_name)
        if self_check == False:
            raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))        
        return super().check_permissions(request)

    def perform_create(self, serializer):
        storage_id = self.request.data.get("pallet_storage_id", None)
        if storage_id == None:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        try:
            storage = Storage.objects.get( pk = storage_id )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        access = None
        # Can be made if user is a owner or employee of this
        if self.is_owner() == True:
            if storage.storage_branch.branch_company.company_owner != self.request.user:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter(access_employee = self.request.user, access_branch = storage.storage_branch).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        # To create pallet instance
        instance = serializer.save()
        # To create for some locations of pallet
        locations = self.request.data.get("pallet_locations", [])
        for location in locations:
            location_serializer = location_serializers.LocationSerializer(data=location)
            location_serializer.is_valid(raise_exception=True)
            location_serializer.save(location_pallet = instance)

    def perform_update(self, serializer):
        # To create pallet instance
        instance = serializer.save()
        # Delete all old location
        try:
            old_locations = Location.objects.filter( location_pallet = instance )
        except:
            pass 
        for old_location in old_locations:
            old_location.delete()
        # To create for some locations of pallet
        locations = self.request.data.get("pallet_locations", [])
        for location in locations:
            location_serializer = location_serializers.LocationSerializer(data=location)
            location_serializer.is_valid(raise_exception=True)
            location_serializer.save(location_pallet = instance)  
        

    def update(self, request, *args, **kwargs):
        if request.data.get("pallet_storage_id", None) != None:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_STORAGE_OF_PALLET))
        try:
            pallet = Pallet.objects.get( pk = self.kwargs["pk"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_PALLET))
        storage = pallet.pallet_storage
        access = None
        # Can be made if user is a owner or employee of this
        if self.is_owner() == True:
            if storage.storage_branch.branch_company.company_owner != self.request.user:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter(access_employee = self.request.user, access_branch = storage.storage_branch).first()
                except:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))      
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            pallet = Pallet.objects.get( pk = self.kwargs["pk"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_PALLET))
        storage = pallet.pallet_storage
        access = None
        # Can be made if user is a owner or employee of this
        if self.is_owner() == True:
            if storage.storage_branch.branch_company.company_owner != self.request.user:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter(access_employee = self.request.user, access_branch = storage.storage_branch).first()
                except:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))        
        return super().destroy(request, *args, **kwargs)
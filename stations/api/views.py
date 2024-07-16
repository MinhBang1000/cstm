# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated

# Customize
from bases.views import BaseViewSet
from bases import errors
from stations.models import Station
from stations.api import serializers as station_serializers
from storages.models import Storage
from storage_accesses.models import StorageAccess
from branch_accesses.models import BranchAccess

class StationViewSet(BaseViewSet):
    serializer_class = station_serializers.StationSerializer
    permission_classes = [ IsAuthenticated ]
    filterset_fields = [ "id","station_username","station_password","station_storage__id" ]
    view_name = "station"

    def get_queryset(self):
        user = self.request.user 
        if self.is_owner() == True:
            return Station.objects.filter( station_storage__storage_branch__branch_company__company_owner = user )
        access = None 
        try:
            access = StorageAccess.objects.filter( access_employee = user ).first()
        except:
            pass 
        if access == None:
            try:
                access = BranchAccess.objects.filter( access_employee = user ).first()
            except:
                pass 
            if access == None:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
            return Station.objects.filter( station_storage__storage_branch = access.access_branch )
        return Station.objects.filter( station_storage = access.access_storage )

    def check_permissions(self, request):
        # To check user permissions - do not review block permissions yet
        # self_check = self.is_permission(self.view_name)
        # if self_check == False:
        #     raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))        
        return super().check_permissions(request)

    def perform_create(self, serializer):
        # Check role have a right permission
        storage_id = self.request.data.get("station_storage_id", None)
        if storage_id == None:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        user = self.request.user 
        try:
            storage = Storage.objects.get( pk = storage_id )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        if self.is_owner() == True:
            if user != storage.storage_branch.branch_company.company_owner:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            access = None 
            try:
                access = StorageAccess.objects.filter( access_employee = user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = user, access_branch = storage.storage_branch ).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        # Check role have a right permission
        try:
            station = Station.objects.get( pk = self.kwargs["pk"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STATION))
        storage = station.station_storage
        user = self.request.user 
        if self.is_owner() == True:
            if user != storage.storage_branch.branch_company.company_owner:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            access = None 
            try:
                access = StorageAccess.objects.filter( access_employee = user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = user, access_branch = storage.storage_branch ).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        # Check role have a right permission
        try:
            station = Station.objects.get( pk = self.kwargs["pk"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STATION))
        storage = station.station_storage
        user = self.request.user 
        if self.is_owner() == True:
            if user != storage.storage_branch.branch_company.company_owner:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            access = None 
            try:
                access = StorageAccess.objects.filter( access_employee = user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = user, access_branch = storage.storage_branch ).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        return super().perform_destroy(instance)
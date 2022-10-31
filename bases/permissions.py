from rest_framework import permissions

class IsAnyOne(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

class IsOwnerManager(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ["Onwer", "Manager","Administrator"]

class IsOwnerAdmin(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ["Owner","Administrator"]

class IsAnonymus(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == "Anonymous"

class IsOwnerAnonymus(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ["Owner","Anonymous","Administrator"]

class IsSupervisor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and request.user.role in ["Supervisor","Administrator"]

class IsOwnerSupervisor(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ["Owner","Supervisor","Administrator"]

class IsOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role.role_creater == -1
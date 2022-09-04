from rest_framework import permissions

class IsOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ["Owner", "Anonymous"]
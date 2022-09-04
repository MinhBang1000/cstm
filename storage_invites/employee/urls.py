# Rest framework
from django.urls import path

# Customize
from storage_invites.employee.views import accept_invite, request_access

urlpatterns = [
    path('<str:storage_code>/', request_access, name="request_access"),
    path('<int:invite_id>/', accept_invite, name="accept_invite")
]
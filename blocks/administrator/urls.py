from django.urls import path
from blocks.administrator.views import block_permission, unblock_permission

urlpatterns = [
    path('block/', block_permission, name="block_permissions"),
    path('unblock/', unblock_permission, name="unblock_permissions"),
]
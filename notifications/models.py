# Django
from django.db import models
from django.contrib.auth import get_user_model

# Customize
from storage_invites.models import StorageEmployee

User = get_user_model()

class Notification(models.Model):

    notification_type = models.CharField(max_length=50, default="None Type")
    notification_title = models.CharField(max_length=250)
    notification_content = models.TextField(max_length=500)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    invite = models.ForeignKey(StorageEmployee, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
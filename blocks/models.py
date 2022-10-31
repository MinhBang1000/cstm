from django.db import models
from django.contrib.auth import get_user_model
from permissions.models import Permission
User = get_user_model()

# Create your models here.
class Block(models.Model):
    block_permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permission_roles")
    block_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blocks")
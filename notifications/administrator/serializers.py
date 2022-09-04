# Rest Framework
from rest_framework import serializers

# Customize
from notifications.models import Notification
from users.employee.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [ "notification_type", "notification_title", "notification_content", "receiver", "invite", "created_at" ]
        read_only_fields = [ "created_at", "invite" ]
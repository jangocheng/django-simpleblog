from . import models
from rest_framework import serializers


class NotificationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = (
            'content',
            'created_time',
        )

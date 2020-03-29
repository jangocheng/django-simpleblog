from . import models
from . import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin


class NotificationViewSet(ListModelMixin, GenericViewSet):
    queryset = models.Notification.objects.filter(is_delete=False, is_show=True).order_by('-order', '-id').all()[0:1]
    serializer_class = serializers.NotificationModelSerializer

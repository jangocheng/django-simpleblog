from . import views
from django.urls import path, include
from utils.router import router

router.register('notification', views.NotificationViewSet, basename='notification-notification')

urlpatterns = [
    path('', include(router.urls))
]

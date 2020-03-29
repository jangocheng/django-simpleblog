from . import models
from django.contrib import admin


class NotificationConfig(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_time', 'updated_time')
    list_display_links = ('id',)
    list_editable = ('content',)
    list_per_page = 10


admin.site.register(models.Notification, NotificationConfig)

from django.db import models
from utils.model import BaseModel


class Notification(BaseModel):
    content = models.CharField(max_length=64, verbose_name='通知内容')

    def __str__(self):
        return self.content[0:20]

    class Meta:
        db_table = 'myblog_notification'
        verbose_name = '通知表'
        verbose_name_plural = verbose_name

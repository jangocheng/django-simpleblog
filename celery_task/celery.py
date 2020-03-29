# 1.加载Django配置环境
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'simpleblog.settings.dev')

# 2.加载Celery配置环境
from celery import Celery

broker = 'redis://127.0.0.1:6379/0'
backend = 'redis://127.0.0.1:6379/1'
app = Celery(broker=broker, backend=backend, include=['celery_task.tasks'])

# 时区
app.conf.timezone = 'Asia/Shanghai'
# UTC
app.conf.enable_utc = False

from datetime import timedelta

app.conf.beat_schedule = {
    'update-article-cache': {
        'task': 'celery_task.tasks.update_article_cache',
        # 每60秒添加一次
        'schedule': timedelta(seconds=60),
        'args': ()
    }
}

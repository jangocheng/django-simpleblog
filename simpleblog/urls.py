from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve

urlpatterns = [
    # 路由分发
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('article/', include('article.urls')),
    path('notification/', include('notification.urls')),
    # markdown编辑器
    path('mdeditor/', include('mdeditor.urls')),


    # 媒体文件
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]

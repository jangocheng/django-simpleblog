from django.urls import path, re_path
from . import views

urlpatterns = [
    # 登陆接口
    path('login/', views.LoginAPIView.as_view()),
    # 手机号登陆接口
    path('login/mobile/', views.LoginMobileAPIView.as_view()),
    # 验证手机号是否已存在接口
    path('mobile/', views.MobileCheckAPIView.as_view()),
    # 发送验证码接口
    path('sms/', views.SMSAPIView.as_view()),
    # 手机号注册接口
    path('register/mobile/', views.RegisterMobileAPIView.as_view()),




]

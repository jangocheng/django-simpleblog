from rest_framework.views import APIView
from . import serializers
from utils.response import APIResponse
import re
from libs import tx_sms
from django.core.cache import cache
from django.conf import settings
from . import models
from . import throttles


class LoginAPIView(APIView):
    # 禁用认证/权限组件
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer_obj = serializers.LoginModelSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        return APIResponse(results={
            'username': serializer_obj.content.get('user').username,
            'token': serializer_obj.content.get('token')
        })


# 手机验证码登录
class LoginMobileAPIView(APIView):
    # 禁用认证/权限组件
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer_obj = serializers.LoginMobileModelSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        return APIResponse(results={
            'username': serializer_obj.content.get('user').username,
            'token': serializer_obj.content.get('token')
        })


# 发送验证码
class SMSAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    # 自定义频率限制
    throttle_classes = (throttles.SMSRateThrottle,)

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile', None)

        if not mobile:
            return APIResponse(1, msg='mobile字段必须', http_status=400)

        if not re.match(r'^1[3-9][0-9]{9}$', mobile):
            return APIResponse(1, msg='mobile格式错误', http_status=400)

        code = tx_sms.get_sms_code()

        result = tx_sms.send_sms_code(mobile, code, settings.SMS_EXP // 60)

        if not result:
            return APIResponse(1, msg='验证码发送失败')

        cache.set(settings.SMS_CACHE_FORMAT % mobile, code, settings.SMS_EXP)

        return APIResponse(0, msg='验证码发送成功')


# 判断手机号是否已经注册
class MobileCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        if not mobile:
            return APIResponse(1, msg='mobile必须提供', http_status=400)

        if not re.match(r'^1[3-9][0-9]{9}$', mobile):
            return APIResponse(1, msg='mobile格式错误', http_status=400)

        try:
            models.User.objects.get(mobile=mobile)
            return APIResponse(2, msg='该号码已注册')
        except:
            return APIResponse(0, msg='该号码未注册')


# 验证码注册
class RegisterMobileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer_obj = serializers.RegisterMobileModelSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        user_obj = serializer_obj.save()
        return APIResponse(results=serializers.RegisterMobileModelSerializer(user_obj).data)

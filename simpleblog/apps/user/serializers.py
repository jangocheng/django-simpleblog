import re
from . import models
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache
from django.conf import settings


class LoginModelSerializer(serializers.ModelSerializer):
    # post请求默认会按照create方法进行校验(注册), 所有我们自定义字段进行简单的校验
    username = serializers.CharField(min_length=3, max_length=16)
    password = serializers.CharField(min_length=6)

    class Meta:
        model = models.User
        fields = ('username', 'password')

    # 完成token的签发
    def validate(self, attrs):
        user = self._validate_user(attrs)
        # 载荷
        payload = jwt_payload_handler(user)
        # token
        token = jwt_encode_handler(payload)
        # 保存到serializer对象中, 以便取用
        self.content = {
            'user': user,
            'token': token
        }
        return attrs

    # 多方式登录
    def _validate_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if re.match(r'.*@.*', username):
            user = models.User.objects.filter(email=username).first()
        elif re.match(r'^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(mobile=username).first()
        else:
            user = models.User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({'message': '用户名或密码错误'})

        return user


# 手机号登陆
class LoginMobileModelSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11)
    code = serializers.CharField(min_length=6)

    class Meta:
        model = models.User
        fields = ('mobile', 'code')

    # 对验证码进行简单的校验
    def validate_code(self, value):
        try:
            int(value)
            return value
        except:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.pop('code')

        # 服务端缓存验证码
        old_code = cache.get(settings.SMS_CACHE_FORMAT % mobile)

        if code != old_code:
            raise serializers.ValidationError({'code': '验证码错误'})

        # 严重么校验通过就失效
        cache.set(settings.SMS_CACHE_FORMAT % mobile, None, 0)

        try:
            user = models.User.objects.get(mobile=mobile, is_active=True)
        except:
            raise serializers.ValidationError({'mobile': '用户不存在'})

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        self.content = {
            'user': user,
            'token': token
        }
        return attrs


# 注册
class RegisterMobileModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=6, max_length=6, write_only=True)

    class Meta:
        model = models.User
        fields = ('username', 'mobile', 'password', 'code')
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    # 对验证码进行简单的校验
    def validate_code(self, value):
        try:
            int(value)
            return value
        except:
            raise serializers.ValidationError('验证码错误')

    # 对手机号码进行简单的校验
    def validae_mobile(self, value):
        if not re.match(r'^1[3-9][0-9]{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    # 判断验证码是否正确
    def validate(self, attrs):
        code = attrs.pop('code')
        mobile = attrs.get('mobile')
        old_code = cache.get(settings.SMS_CACHE_FORMAT % mobile)

        if code != old_code:
            raise serializers.ValidationError({'code': '验证码错误'})

        # 验证码校验通过就失效
        cache.set(settings.SMS_CACHE_FORMAT % mobile, None, 0)

        attrs['username'] = mobile[-4:]
        return attrs

    # 重写create方法实现密码密文入库
    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)

from rest_framework.throttling import SimpleRateThrottle


# 对验证码接口进行频率限制
class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile') or request.data.get('mobile')
        # 没提供手机号就不作限制
        if not mobile:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': mobile
        }

import random
from qcloudsms_py import SmsSingleSender
from . import settings
from utils.logging import logger


# 生成6位随机验证码
def get_sms_code():
    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    return code


# 发送随机验证码
def send_sms_code(mobile, code, exp):
    sender = SmsSingleSender(settings.APP_ID, settings.APP_KEY)
    try:
        response = sender.send_with_param(86, mobile,
                                          settings.TEMPLATE_ID, (code, exp), sign=settings.SMS_SIGN, extend="", ext="")

        # {'result': 0, 'errmsg': 'OK', 'ext': '', 'sid': '8:7WTQN1E7dYVx3XW9dzl20200107', 'fee': 1}
        if response and response.get('result') == 0:
            return True

        logger.error(f"信息发送失败, 状态码:{response.get('result')}, 错误信息:{response.get('errmsg')}")

    except Exception as e:
        logger.error(f"信息发送异常, 异常信息:{e}")
    return False

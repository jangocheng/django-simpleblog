from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from .logging import logger


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    # 按照一定格式返回异常信息: 视图对象---请求方法---错误对象
    detail = f"{context.get('view')}---{context.get('request')}---{exc}"

    # drf的异常模块不会处理服务端的异常
    if not response:
        response = Response(data={'detail': detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response.data = {'detail': detail}
    # 将异常信息记录到日志中
    logger.critical(response.data.get('detail'))

    return response

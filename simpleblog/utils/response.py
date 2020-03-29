from rest_framework.response import Response


class APIResponse(Response):
    # 重写__init__方法
    def __init__(self, status=0, msg='ok', results=None, http_status=None, template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        # 将status, msg, results, kwargs添加到data当中
        data = {
            'status': status,
            'msg': msg
        }

        if results is not None:
            data['results'] = results

        data.update(kwargs)

        super().__init__(data=data, status=http_status, template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)

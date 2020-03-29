from rest_framework import pagination


# 自定义分页类继承PageNumberPagination, 然后完成配置即可
class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 2

    page_query_param = 'page'

    page_size_query_param = 'page_size'

    max_page_size = 10


# 自定义偏移分页继承LimitOffsetPagination, 然后完成配置
class LimitOffsetPagination(pagination.LimitOffsetPagination):
    # 默认一页显示的条数
    default_limit = 2
    # 用户自定义一页显示的条数
    limit_query_param = 'limit'
    # 用户自定义偏移的条数
    offset_query_param = 'offset'
    # 用户最大可自定义一页显示的条数
    max_limit = 3

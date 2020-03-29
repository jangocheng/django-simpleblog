from . import filters
from . import models
from . import paginations
from . import serializers
from django.db.models import F
from django.core.cache import cache
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoryListViewSet(ListModelMixin, GenericViewSet):
    """分类群查"""
    queryset = models.Category.objects.filter(is_delete=False, is_show=True).order_by('-order').all()
    serializer_class = serializers.CategoryModelSerializer


class ArticleViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """文章群查/单查/"""
    queryset = models.Article.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.ArticleModelSerializer

    # 配置自定义分页类
    pagination_class = paginations.PageNumberPagination
    # 配置过滤类
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # 设置参与搜索的字段, 如果不设置, 则默认为序列化类中所配置的字段都参与搜索
    search_fields = ['title', 'about']
    # 设置参与排序的字段
    ordering_fields = ['view_count', 'like_count', 'comment_count', 'id']
    # 配置自定义过滤类
    filter_class = filters.ArticleFilterSet

    # 重写list方法实现从缓存中获取数据
    def list(self, request, *args, **kwargs):
        article_data = cache.get('article_cache')
        print(article_data)
        # 首页默认url参数
        home_page_params = {'ordering': ['-id'], 'page_size': ['5'], 'page': ['1']}
        # 缓存中没有数据或者不是默认url参数的请求则从数据库中获取, 比如用户选择了分类, 排序和分页
        if not article_data or dict(request.GET) != home_page_params:
            response = super().list(request, *args, **kwargs)
            # 只将携带默认参数的请求的数据放入缓存中
            if dict(request.GET) == home_page_params:
                cache.set('article_cache', response.data)
            article_data = response.data
        return Response(article_data)

    # 自定义retrieve方法实现文章浏览量的增加
    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        models.Article.objects.filter(pk=article.id).update(view_count=F('view_count') + 1)
        return super().retrieve(request, *args, **kwargs)


class SearchArticleListViewSet(ListModelMixin, GenericViewSet):
    """搜索文章"""
    queryset = models.Article.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.ArticleModelSerializer

    filter_backends = [SearchFilter]
    search_fields = ('title',)
    pagination_class = paginations.PageNumberPagination


class ArticleUpdateViewSet(UpdateModelMixin, GenericViewSet):
    """修改文章(点赞)"""
    queryset = models.Article.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.ArticleModelSerializer


class CommentViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """评论查询/添加"""
    queryset = models.Comment.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.CommentModelSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.CommentFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        article_id = request.data.get('belong')
        models.Article.objects.filter(is_delete=False, is_show=True, pk=article_id).update(
            comment_count=F('comment_count') + 1)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ArchiveAndAboutViewSet(ListModelMixin, GenericViewSet):
    """
    归档/关于: 归档的文章category_id为1, 关于的文章category_id为2
    设置is_show=False使其不在首页显示
    """
    queryset = models.Article.objects.filter(is_delete=False).all()
    serializer_class = serializers.ArticleModelSerializer

    filter_backends = [DjangoFilterBackend]
    filter_class = filters.ArticleFilterSet



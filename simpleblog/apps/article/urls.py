from . import views
from django.urls import path, include
from utils.router import router

router.register('categories', views.CategoryListViewSet, basename='article-categories')
router.register('articles', views.ArticleViewSet, basename='article-articles')
router.register('search', views.SearchArticleListViewSet, basename='article-search')
router.register('likes', views.ArticleUpdateViewSet, basename='article-likes')
router.register('comments', views.CommentViewSet, basename='article-comments')
router.register('archive', views.ArchiveAndAboutViewSet, basename='article-archive')

urlpatterns = [
    path('', include(router.urls))
]

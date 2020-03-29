from .celery import app
from article.models import Article
from article.serializers import ArticleModelSerializer
from django.conf import settings
from django.core.cache import cache


@app.task
def update_article_cache():
    queryset = Article.objects.filter(is_delete=False, is_show=True).order_by('-id').all()
    serializer_obj = ArticleModelSerializer(queryset, many=True)

    # 数据结构和view.py中保存一致
    article_data_ = {
        'count': len(serializer_obj.data),
        'next': f'{settings.BASE_URL}/article/articles/?ordering=-id&page=2&page_size=5',
        'previous': None,
        'results': serializer_obj.data[0:5]
    }
    cache.set('article_cache', article_data_)

    return True

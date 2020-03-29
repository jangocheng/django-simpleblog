from . import models
from django_filters.filterset import FilterSet


class ArticleFilterSet(FilterSet):
    class Meta:
        model = models.Article
        fields = ('category', 'tags')


class CommentFilter(FilterSet):
    class Meta:
        model = models.Comment
        fields = ('belong',)


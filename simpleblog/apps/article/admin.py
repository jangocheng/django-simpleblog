from . import models
from django.contrib import admin


class ArticleConfig(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'about', 'cover', 'category', 'view_count', 'like_count', 'created_time', 'updated_time'
    )
    list_display_links = ('id',)
    search_fields = ('title',)
    list_editable = ('title', 'about', 'cover', 'view_count', 'like_count')
    list_per_page = 10


class CategoryAndTagConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_time', 'updated_time')
    list_display_links = ('id',)
    list_editable = ('name',)
    list_per_page = 10


class Article2TagConfig(admin.ModelAdmin):
    list_display = ('id', 'article', 'tag', 'created_time', 'updated_time')
    list_display_links = ('id',)
    search_fields = ('id',)
    list_editable = ('article', 'tag')
    list_per_page = 10


admin.site.register(models.Article, ArticleConfig)
admin.site.register(models.Category, CategoryAndTagConfig)
admin.site.register(models.Tag, CategoryAndTagConfig)
admin.site.register(models.Article2Tag, Article2TagConfig)
admin.site.register(models.Comment)

admin.site.site_title = '洛碧兰德'
admin.site.site_header = '洛碧兰德'

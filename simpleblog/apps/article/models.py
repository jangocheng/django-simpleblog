from mdeditor.fields import MDTextField
from django.db import models
from django.conf import settings
from markdown import markdown
from user.models import User
from utils.model import BaseModel


class Article(BaseModel):
    """文章"""
    title = models.CharField(max_length=32, verbose_name='文章标题')
    cover = models.CharField(max_length=255, default='https://lowbeeland.oss-cn-shanghai.aliyuncs.com/default.png',
                             verbose_name='文章封面')
    about = models.CharField(max_length=128, verbose_name='文章简介')
    content = MDTextField(verbose_name='文章内容')
    view_count = models.IntegerField(default=0, blank=True, verbose_name='阅读数量')
    like_count = models.IntegerField(default=0, blank=True, verbose_name='点赞数量')
    comment_count = models.IntegerField(default=0, blank=True, verbose_name='评论数量')
    author = models.ForeignKey(to=User, db_constraint=False, on_delete=models.DO_NOTHING, related_name='articles',
                               verbose_name='文章作者')
    category = models.ForeignKey(to='Category', db_constraint=False, on_delete=models.DO_NOTHING,
                                 related_name='articles', verbose_name='文章分类')
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'),
                                  related_name='articles', verbose_name='文章标签')

    @property
    def article_content(self):
        # markdown to html
        article_content = markdown(self.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return article_content

    class Meta:
        db_table = 'simpleblog_article'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Category(BaseModel):
    """分类"""
    name = models.CharField(max_length=32, unique=True, verbose_name='分类名')

    class Meta:
        db_table = 'simpleblog_category'
        verbose_name = '分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BaseComment(BaseModel):
    """评论基表"""
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    parent = models.ForeignKey(to='self', null=True, blank=True, db_constraint=False, on_delete=models.CASCADE,
                               related_name='child', verbose_name='父评论')
    reply_to = models.ForeignKey(to='self', null=True, blank=True, db_constraint=False, on_delete=models.CASCADE,
                                 related_name='relied_by', verbose_name='回复')

    @property
    def comment_user(self):
        username = self.user.username
        comment_user = {
            'username': username,
        }
        return comment_user

    @property
    def reply_to_comment_user(self):
        return self.reply_to.user.username

    class Meta:
        abstract = True

    def ___str__(self):
        return self.content[0:20]


class Comment(BaseComment):
    """评论"""
    belong = models.ForeignKey(to=Article, db_constraint=False, on_delete=models.CASCADE, related_name='comments',
                               verbose_name='所属文章')

    class Meta:
        db_table = 'simpleblog_comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name


class Tag(BaseModel):
    """标签"""
    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')

    class Meta:
        db_table = 'simpleblog_tag'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article2Tag(BaseModel):
    """文章与标签关系表"""
    article = models.ForeignKey(to=Article, db_constraint=False, on_delete=models.CASCADE, verbose_name='文章')
    tag = models.ForeignKey(to=Tag, db_constraint=False, on_delete=models.CASCADE, verbose_name='标签')

    def __str__(self):
        return f'{self.article.title}-{self.tag.name}'

    class Meta:
        db_table = 'simpleblog_article2tag'
        verbose_name = '文章与标签关系表'
        verbose_name_plural = verbose_name

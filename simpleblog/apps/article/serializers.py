from . import models
from rest_framework import serializers


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'id',
            'name',
        )


class UserModelSerializer(serializers.ModelSerializer):
    """文章作者子序列化"""

    class Meta:
        model = models.User
        fields = (
            'username',
        )


class TagModelSerializer(serializers.ModelSerializer):
    """文章标签子序列化"""

    class Meta:
        model = models.Tag
        fields = (
            'id',
            'name',
        )


class ArticleModelSerializer(serializers.ModelSerializer):
    author = UserModelSerializer()
    tags = TagModelSerializer(many=True)

    class Meta:
        model = models.Article
        fields = (
            'id',
            'title',
            'cover',
            'about',
            'article_content',
            'author',
            'tags',
            'comment_count',
            'view_count',
            'like_count',
            'created_time',
            'updated_time'
        )


class CommentModelSerializer(serializers.ModelSerializer):
    comment_user = UserModelSerializer

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'content',
            'belong',
            'comment_user',
            'created_time',
            'parent',
            'reply_to',
            'reply_to_comment_user',
        )
        extra_kwargs = {
            'id': {
                'read_only': True,

            },
            'created_time': {
                'read_only': True,

            },
            'comment_user': {
                'read_only': True,
            },
            'parent': {
                'required': False
            },
            'reply_to': {
                'write_only': True,
                'required': False
            },
            'belong': {
                'write_only': True,
            },
            'reply_to_comment_user': {
                'read_only': True
            },
        }

    def _get_user(self):
        """获取评论用户"""
        return self.context.get('request').user

    def validate(self, attrs):
        """将user添加到attrs中"""
        user = self._get_user()
        attrs['user'] = user
        return attrs

from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Blog, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "author",
            "published_at",
            "created_at",
            "updated_at",
            "comment_count",
        ]


class CommentSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(many=False, read_only=True)
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "blog",
            "author",
        ]

from rest_framework import serializers

from users.serializers import UserSerializer

from .models import BlogComment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent_user = serializers.SerializerMethodField()
    comment_html = serializers.CharField()

    class Meta:
        model = BlogComment
        fields = [
            "id",
            "user",
            "parent",
            "parent_user",
            "comment_html",
            "submit_date",
        ]

        extra_kwargs = {"submit_date": {"format": "%Y-%m-%d %H:%M:%S"}}

    def get_parent_user(self, obj):
        if obj.parent:
            return UserSerializer(obj.parent.user).data


class TreeCommentSerializer(serializers.ModelSerializer):
    descendants = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    comment_html = serializers.CharField()

    class Meta:
        model = BlogComment
        fields = [
            "id",
            "comment_html",
            "submit_date",
            "user",
            "parent",
            "descendants",
        ]
        extra_kwargs = {"submit_date": {"format": "%Y-%m-%d %H:%M:%S"}}

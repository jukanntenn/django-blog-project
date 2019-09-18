from rest_framework import serializers

from users.serializers import UserDetailSerializer

from .models import BlogComment


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    parent_user = serializers.SerializerMethodField()
    comment = serializers.CharField(source='comment_html')

    class Meta:
        model = BlogComment
        fields = [
            'id',
            'comment',
            'user',
            'parent_user',
            'submit_date',
            'parent',
            'name',
        ]

        extra_kwargs = {
            'submit_date': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def get_parent_user(self, obj):
        if obj.parent:
            return UserDetailSerializer(obj.parent.user).data

    def save(self, **kwargs):
        comment = kwargs.pop('comment')
        comment.save()
        # 必须设置 instance 用于序列化
        self.instance = comment
        return comment


class TreeCommentSerializer(serializers.ModelSerializer):
    descendants = serializers.SerializerMethodField()
    user = UserDetailSerializer(required=False)
    comment = serializers.CharField(source='comment_html')

    class Meta:
        model = BlogComment
        fields = [
            'id',
            'comment',
            'submit_date',
            'user',
            'name',
            'parent',
            'descendants',
        ]
        extra_kwargs = {
            'submit_date': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def get_descendants(self, obj):
        qs = obj.descendants
        return CommentSerializer(instance=qs, many=True).data

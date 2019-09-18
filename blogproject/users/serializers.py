from rest_framework import serializers
from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    mugshot = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'mugshot',
        ]

    def get_mugshot(self, obj):
        return obj.social_avatar()

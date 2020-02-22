from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "avatar_url",
        ]

    def get_avatar_url(self, obj):
        try:
            socialaccount = obj.socialaccounts[0]
        except AttributeError:
            socialaccount = obj.socialaccount_set.first()
        except IndexError:
            return ""
        return socialaccount.get_avatar_url()

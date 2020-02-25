from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        name = data.get("name")

        if name:
            try:
                User.objects.get(name=name)
                name = "%s_%s" % (name, sociallogin.account.provider)
                user_field(user, "name", name)
            except User.DoesNotExist:
                user_field(user, "name", name)
        else:
            name = user.username
            user_field(user, "name", name)
        return user

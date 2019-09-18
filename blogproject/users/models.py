from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_('name'), blank=True, max_length=255)
    email_bound = models.BooleanField(_('email bound'), default=False)

    def social_avatar(self):
        if self.socialaccount_set.exists():
            return self.socialaccount_set.first().get_avatar_url()
        return ''


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

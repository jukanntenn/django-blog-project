from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from users.models import User


class Command(BaseCommand):
    help = 'Create DRF Token for all users'

    def handle(self, *args, **options):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
        self.stdout.write('Done!')

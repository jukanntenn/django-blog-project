from celery import shared_task
from django.core.management import call_command


# https://django-dbbackup.readthedocs.io/en/master/commands.html#dbbackup
@shared_task
def dbbackup():
    return call_command("dbbackup", "--clean")


# https://django-dbbackup.readthedocs.io/en/master/commands.html#mediabackup
@shared_task
def mediabackup():
    return call_command("mediabackup", "--clean")

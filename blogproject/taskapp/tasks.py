from celery import shared_task
from django.core.management import call_command


@shared_task
def dbbackup():
    return call_command("dbbackup")


@shared_task
def mediabackup():
    return call_command("mediabackup")

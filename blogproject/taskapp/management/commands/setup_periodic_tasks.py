from django.core.management.base import BaseCommand
from django.db import transaction
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask

from blogproject.taskapp.tasks import dbbackup, mediabackup


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {dbbackup.name}
    - {mediabackup.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print("Deleting all periodic tasks and schedules...\n")

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                "task": dbbackup,
                "name": "Backup database",
                # https://crontab.guru/every-day-at-midnight
                "cron": {
                    "minute": "0",
                    "hour": "0",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
            },
            {
                "task": mediabackup,
                "name": "Backup media files",
                # https://crontab.guru/every-day-at-midnight
                "cron": {
                    "minute": "0",
                    "hour": "0",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(**periodic_task["cron"])

            PeriodicTask.objects.create(
                name=periodic_task["name"],
                task=periodic_task["task"].name,
                crontab=cron,
                enabled=periodic_task["enabled"],
            )

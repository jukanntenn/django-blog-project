#!/bin/bash

rm -f './celerybeat.pid'
celery -A blogproject.taskapp beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

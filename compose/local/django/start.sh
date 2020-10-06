#!/bin/sh

python manage.py compilemessages
python manage.py migrate
python manage.py setup_periodic_tasks
python manage.py runserver 0.0.0.0:8000

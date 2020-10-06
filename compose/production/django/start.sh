#!/bin/sh

python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py migrate
python manage.py setup_periodic_tasks
gunicorn config.asgi:application -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --chdir=/app
FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext python3-dev libpq-dev wget
RUN wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
RUN bash -c "echo deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main >> /etc/apt/sources.list.d/pgdg.list"
RUN apt-get update && apt-get -y install postgresql-client-12

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "/root/.poetry/bin:${PATH}"
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root --no-interaction --no-dev

COPY . /app
RUN poetry install --no-dev --no-interaction

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

COPY ./compose/production/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/production/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

ENTRYPOINT ["/entrypoint.sh"]
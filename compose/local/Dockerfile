FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev gcc \
  # Translations dependencies
  && apk add gettext

RUN apk add musl-dev

WORKDIR /app

RUN pip3 install pip --upgrade -i https://pypi.douban.com/simple
RUN pip3 install pipenv -i https://pypi.douban.com/simple

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --dev --ignore-pipfile

COPY ./compose/local/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
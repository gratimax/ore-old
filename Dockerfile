FROM ubuntu:14.04
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN apt-get update
RUN apt install -y python3-dev python3-pip libpq-dev

ADD . /code
WORKDIR /code

RUN pip3 install -r requirements/production.txt

ENV DJANGO_SETTINGS_MODULE ore.settings.production

EXPOSE 80
CMD gunicorn -w 3 -b 0.0.0.0:80 ore.wsgi

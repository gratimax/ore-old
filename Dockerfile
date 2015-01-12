FROM ubuntu:14.04
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN apt-get update
RUN apt install -y python3-dev python3-pip libpq-dev

ADD requirements/ /code/requirements/
WORKDIR /code
RUN pip3 install -r requirements/staging.txt


ADD . /code

ENV DJANGO_SETTINGS_MODULE ore.settings.collectstatic
RUN echo 'yes' | python3 manage.py collectstatic

ENV DJANGO_SETTINGS_MODULE ore.settings.staging

EXPOSE 80
CMD gunicorn -w 3 -b 0.0.0.0:80 ore.wsgi --log-file -

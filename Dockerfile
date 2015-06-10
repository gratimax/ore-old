FROM python:3.4
MAINTAINER Sponge Web Team <web@spongepowered.org>

ADD requirements/ /code/requirements/
WORKDIR /code

RUN pip install -r /code/requirements/staging.txt

ADD . /code

EXPOSE 3000
CMD gunicorn -w 3 -b 0.0.0.0:3000 ore.wsgi --log-file -

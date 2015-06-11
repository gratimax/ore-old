FROM spongepowered/python3.4-sass
MAINTAINER Sponge Web Team <web@spongepowered.org>

ADD requirements/ /app/requirements/
WORKDIR /app

RUN pip install -r /app/requirements/staging.txt

ADD . /app

EXPOSE 3000
CMD gunicorn -w 3 -b 0.0.0.0:3000 ore.wsgi --log-file -

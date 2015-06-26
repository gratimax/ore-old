FROM spongepowered/ore-base
MAINTAINER Sponge Web Team <web@spongepowered.org>

EXPOSE 3000
CMD ["gunicorn","-w","3","-b","0.0.0.0:3000","ore.wsgi","--log-file","-"]

WORKDIR /app

ADD requirements/ /app/requirements/
RUN pip3 install -r requirements/docker.txt

ADD . /app
RUN \
    DJANGO_SETTINGS_MODULE=ore.settings.docker \
    SECRET_KEY=lemons \
    DB_USER=lemons \
    DB_PASSWORD=lemons \
    DB_HOST=lemons \
    python3 -m ore.manage bower_install

FROM spongepowered/ore-base
MAINTAINER Sponge Web Team <web@spongepowered.org>

EXPOSE 3000
CMD ["gunicorn","-w","3","-b","0.0.0.0:3000","ore.wsgi","--log-file","-"]

WORKDIR /app

COPY requirements/ /app/requirements/
RUN pip3 install --find-links https://repo.spongepowered.org/wheels/ -r requirements/docker.txt

COPY . /app
ENV DJANGO_SETTINGS_MODULE=ore.settings.docker \
    SECRET_KEY=lemons \
    DB_NAME=lemons \
    DB_USER=lemons \
    DB_PASSWORD=lemons \
    DB_HOST=lemons

RUN ([ "$BUILD_VCS_NUMBER_ore_Ore" ] && echo ${BUILD_VCS_NUMBER_ore_Ore:0:7} > APP-VERSION || \
    git rev-parse --short HEAD > APP-VERSION) && \
    bower install

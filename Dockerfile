FROM spongepowered/python3.4-sass
MAINTAINER Sponge Web Team <web@spongepowered.org>

EXPOSE 3000
CMD ["gunicorn","-w","3","-b","0.0.0.0:3000","ore.wsgi","--log-file","-"]

WORKDIR /app

ADD requirements/ /app/requirements/
RUN pip install -r /app/requirements/staging.txt

ADD . /app
RUN sed -i 's/BOWER_COMPONENTS_ROOT = STATIC_ROOT/BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, "bower")/' /app/ore/settings/base.py && apt-get update && apt-get install -y npm && npm install -g bower && sed -i -e 's/env node/env nodejs/' -e 's/rootCheck(/\/\/rootCheck(/' /usr/local/lib/node_modules/bower/bin/bower && cd /app && DJANGO_SETTINGS_MODULE=ore.settings.staging SECRET_KEY=lemons DB_USER=lemons DB_PASSWORD=lemons DB_HOST=lemons python3.4 -m ore.manage bower_install && apt-get remove -y npm && apt-get autoremove -y && rm -rf /usr/local/{lib/node{,/.npm,_modules},bin,share/man}/{npm,bower}* /var/lib/apt/lists/*

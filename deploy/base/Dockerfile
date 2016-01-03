FROM debian:jessie
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN \
    apt-get update && \
    apt-get install -y python3-wheel python3-pip libpq5 git nodejs npm libjpeg62-turbo libpng12-0 zlib1g libwebp5 libopenjpeg5 liblcms2-2 libtiff5 libfreetype6 && \
    ln -s /usr/bin/nodejs /usr/bin/node && \
    npm install -g bower && \
    echo "{ \"allow_root\": true }" > /root/.bowerrc && \
    rm -rf /var/lib/apt/lists/*

FROM debian:jessie
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN \
    apt-get update && \
    apt-get install -y python3-dev python3-pip libpq-dev git nodejs npm && \
    ln -s /usr/bin/nodejs /usr/bin/node && \
    npm install -g bower && \
    echo "{ \"allow_root\": true }" > /root/.bowerrc

FROM debian:jessie
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN \
    apt-get update && \
    apt-get install -y python3-dev python3-pip npm && \
    npm install -g bower && \
    echo "{ \"allow_root\": true }" > /root/.bowerrc

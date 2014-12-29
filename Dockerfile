FROM debian:jessie
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN apt update
RUN apt install -y python-dev python-pip libpq-dev

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 80
CMD python run.py

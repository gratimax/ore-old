FROM ubuntu:14.04
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN apt-get update
RUN apt-get install -y python python-dev python-pip libpq-dev

RUN pip install virtualenv

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 80
CMD python run.py

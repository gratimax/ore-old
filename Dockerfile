FROM debian:jessie
MAINTAINER Sponge Web Team <web@spongepowered.org>

RUN apt update
RUN apt install -y python python-pip

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 80
CMD python run.py

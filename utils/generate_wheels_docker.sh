#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR=$(readlink -f $DIR/..)
IMAGE=$(cat $BASEDIR/deploy/base/Dockerfile | grep 'FROM ' | awk '{print $2}')
ENVIRONMENT=base

ARG=$1
shift 1
if [[ $ARG == "inside" ]]; then
	set -e

	cd $DIR

	apt-get update
	apt-get -y install python3 python3-pip 
	apt-get -y install libjpeg-dev libpng-dev libz-dev libwebp-dev libopenjpeg-dev liblcms2-dev libtiff-dev libfreetype6-dev libpq-dev git
	ln -s /usr/bin/pip3 /usr/bin/pip
	exec $DIR/generate_wheels.sh "$@"
else
	exec docker run --rm=true -v $BASEDIR:/work debian:jessie /work/$(basename $DIR)/generate_wheels_docker.sh inside $ENVIRONMENT
fi

FROM ubuntu:16.04
LABEL maintainer="Ian Rees <ian@interline.io>,Drew Dara-Abrams <drew@interline.io>"

RUN apt-get update -y
RUN apt-get install \
      python \
      python-boto3 \
      curl \
      wget \
      osmosis \
      osmctools \
      parallel \
      awscli \
      software-properties-common \
      -y

COPY scripts /scripts

WORKDIR /app

CMD [ "/usr/bin/python", "/scripts/update_planet.py", "planet-latest.osm.pbf", "planet-new.osm.pbf" ]

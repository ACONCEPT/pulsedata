#! /bin/bash

docker build -t pulsedata/source:1.1 source
docker build -t pulsedata/mongo:1.1 mongo
docker build -t pulsedata/connect:1.1 connect
# the spotify/kafka container works out of the box, no need to build
docker build -t pulsedata/sink:1.1 sink

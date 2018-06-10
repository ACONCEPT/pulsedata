#! /usr/bin/env bash
docker rm pd_sink
docker build -t pulsedata/sink:1.1 sink


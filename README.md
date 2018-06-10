# pulseData Data Engineering Project

This directory contains the code and configuration for a sample data
pipeline. Your task is to investigate the pipeline and create a report
summarizing any issues that you find along with your suggestions for
how to fix them. You should also take notes while investigating the
pipeline to record your process the best you can. We're just as
interested in how you approach a problem as we are in the solution.


## Overview

The pipeline consists of five parts, each one in its own docker
container. Here is just a short summary of each container and all of
the details can be found in source code.

#### source

The `source` container runs a python program that generates random
profile data and inserts it into the mongo database. The network
settings for this container can be intentially modified to simulate
a poor network in an effort to exaggerate any issues that might arise.
See `write_profile_data.sh` for more details.

#### mongo

The `mongo` container runs a mongo database. It is a single node, but
it has been configured to run as a replica set so that
the [oplog](https://docs.mongodb.com/v3.4/core/replica-set-oplog/) is
enabled.

#### connect

The `connect` container runs [kafka-connect-mongodb](https://github.com/DataReply/kafka-connect-mongodb).
This is a connector for [Kafka Connect](https://docs.confluent.io/current/connect/index.html).
It is a java program that tails the mongo oplog and writes new entries
into a kafka topic.

This container is slow to startup compared to the other containers.

#### kafka

The `kafka` container runs the
[spotify/kafka](https://github.com/spotify/docker-kafka) image.  This
is a simplified installation of kafka that runs both zookeeper and
kafka in the same container.

#### sink

The `sink` container runs a python program that is a kafka
consumer. It logs each received profile.


## Running

The pipeline can be launched with `docker-compose up`. You might need
to install `docker-compose`; instructions can be found
https://docs.docker.com/compose/install/.

All of the containers have been published to
[https://hub.docker.com/u/pulsedata/](https://hub.docker.com/u/pulsedata/)
but you can also build them on your own if you'd like. Run `build.sh`
to do so. The `connect` container is particularly slow to build
though.

You can check that the pipeline has come up by first checking that all
of the containers have started:

```
$ docker ps
```
```
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                NAMES
3cadc4426b45        spotify/kafka           "supervisord -n"         20 minutes ago      Up 27 seconds       2181/tcp, 9092/tcp   pd_kafka
711ed071a368        pulsedata/sink:1.1      "/bin/sh -c 'python3…"   20 minutes ago      Up 27 seconds                            pd_sink
26e3d962cff1        pulsedata/connect:1.1   "/bin/sh -c /usr/loc…"   20 minutes ago      Up 27 seconds       8083/tcp, 9092/tcp   pd_kafka-connect
fa1ad9825c6d        pulsedata/mongo:1.1     "/usr/local/bin/my-e…"   20 minutes ago      Up 27 seconds       27017/tcp            pd_mongo
0c50c51820c9        pulsedata/source:1.1    "/bin/sh -c /usr/loc…"   20 minutes ago      Up 27 seconds                            pd_source
```

And, then query mongo to see that it has profile data:
```
$ docker exec -i pd_mongo mongo pulsedata <<EOF
db.profiles.findOne()
EOF
```
The profile data is random, but you should see results that look like:
```
MongoDB shell version v3.4.14
connecting to: mongodb://127.0.0.1:27017/pulsedata
MongoDB server version: 3.4.14
{
	"_id" : ObjectId("5ad9fd1375e13d000813fbe6"),
	"email" : "guerragabrielle@yahoo.com",
	"name" : "Patrick Kramer",
	"user_id" : 1,
	"creation_ts" : ISODate("2018-04-20T14:45:39.814Z")
}
bye
```

And, finally, consume the kafka topic
```
$ docker exec -i pd_kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --topic mongo_pulsedata_profiles --bootstrap-server kafka:9092 --max-messages 1 --from-beginning | jq
```
```
{
  "schema": {
    "type": "struct",
    "fields": [
      {
        "type": "int32",
        "optional": true,
        "field": "timestamp"
      },
      {
        "type": "int32",
        "optional": true,
        "field": "order"
      },
      {
        "type": "string",
        "optional": true,
        "field": "operation"
      },
      {
        "type": "string",
        "optional": true,
        "field": "database"
      },
      {
        "type": "string",
        "optional": true,
        "field": "object"
      }
    ],
    "optional": false,
    "name": "mongodbschema_pulsedata_profiles"
  },
  "payload": {
    "timestamp": 1524235539,
    "order": 3,
    "operation": "i",
    "database": "pulsedata.profiles",
    "object": "{ \"_id\" : { \"$oid\" : \"5ad9fd1375e13d000813fbe6\" }, \"email\" : \"guerragabrielle@yahoo.com\", \"name\" : \"Patrick Kramer\", \"user_id\" : 1, \"creation_ts\" : { \"$date\" : 1524235539814 } }"
  }
}
Processed a total of 1 messages
```

It should be straightforward to get the pipeline running; if you have
issues starting the pipeline, please email jobevers@pulsedata.io.

## Notes

If this were a production system, any investigation would be
complicated by the need to prevent data loss. For this exercise, that
is not a requirement. Feel free to modify the configuration and source
code for any of the containers as need to help your investigation.

As a hint to get started: let the pipeline run for a few minutes and
then consume the kafka topic looking at the overall throughput,
latency and and check for possible errors such as duplicate or missing
records.

`docker-compose` creates a new network named `pd_default`. And all of
the containers are available on that network by their name. This means
that you can launch a new container and use it to access the other
services.  For example:

```
$ docker run -it --rm --network=pd_default ubuntu:16.04 /bin/bash
root@ba77bb521139:/# apt-get update -qq
root@ba77bb521139:/# apt-get install -yqq inetutils-ping
[...]

root@ba77bb521139:/# ping -c 3 kafka
PING kafka (172.18.0.4): 56 data bytes
64 bytes from 172.18.0.4: icmp_seq=0 ttl=64 time=0.170 ms
64 bytes from 172.18.0.4: icmp_seq=1 ttl=64 time=0.071 ms
64 bytes from 172.18.0.4: icmp_seq=2 ttl=64 time=0.073 ms
--- kafka ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.071/0.105/0.170/0.046 ms

root@ba77bb521139:/# ping -c 3 mongo
PING mongo (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: icmp_seq=0 ttl=64 time=0.105 ms
64 bytes from 172.18.0.2: icmp_seq=1 ttl=64 time=0.053 ms
64 bytes from 172.18.0.2: icmp_seq=2 ttl=64 time=0.077 ms
--- mongo ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.053/0.078/0.105/0.000 ms
```

### Logs

When `docker-compose up` is run, it mixes together the outputs from
each container, which can be hard to read.  The log for each container can be
accessed using the `docker logs` command.  For example:

```
docker logs --tail 100 -f pd_mongo
```

will output and follow just the logs for the mongo container.

#!/bin/bash
set -Eeuo pipefail

# Start a forked mongo so that we can initialize the replica set
pidfile=/tmp/mongod.pid
mongod --pidfilepath $pidfile --replSet rs0 --logpath /tmp/mongo.log --fork --bind_ip=127.0.0.1,mongo
mongo=( mongo --host 127.0.0.1 --port 27017 --quiet )
tries=30
while true; do
	if ! { [ -s "$pidfile" ] && ps "$(< "$pidfile")" &> /dev/null; }; then
		# bail ASAP if "mongod" isn't even running
		echo >&2
		echo >&2 "error: $originalArgOne does not appear to have stayed running -- perhaps it had an error?"
		echo >&2
		exit 1
	fi
	if "${mongo[@]}" 'admin' --eval 'quit(0)' &> /dev/null; then
		# success!
		break
	fi
	(( tries-- ))
	if [ "$tries" -le 0 ]; then
		echo >&2
		echo >&2 "error: $originalArgOne does not appear to have accepted connections quickly enough -- perhaps it had an error?"
		echo >&2
		exit 1
	fi
	sleep 1
done
"${mongo[@]}" <<EOF
rs.initiate({_id: "rs0", version: 1, members: [{_id: 0, host: "mongo:27017"}]})
EOF
mongod --pidfilepath $pidfile --shutdown

# now start un-forked so that the process is tied to the container
mongod --replSet rs0 --bind_ip=127.0.0.1,mongo

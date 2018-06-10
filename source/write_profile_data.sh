#! /bin/sh

# The network connection between containers in a docker network is
# reliable enough that any mistakes in handling poor network
# conditions will rarely ever show up and can be hard to debug.
#
# One way to debug a pipeline is to force a bad network
# connection. Netflix popularized this idea with Chaos Monkey and the
# Simian Army.
#
# https://github.com/tylertreat/comcast is a tool that is "designed to
# simulate common network problems like latency, bandwidth
# restrictions, and dropped/reordered/corrupted packets."
# Unfortunately, the network level interactions between docker and the
# host OS are complicated and I've found that the line below only
# works when the host OS is linux.
#
# Uncomment this line to drop packets and force network timeouts.
/opt/go/bin/comcast --packet-loss=20%
/opt/venvs/mongo_source/bin/python3 /opt/venvs/mongo_source/scripts/write_profile_data.py 2>&1

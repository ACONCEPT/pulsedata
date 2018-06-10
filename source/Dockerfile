FROM ubuntu:16.04
MAINTAINER Job Evers-Meltzer

ENV PATH="/opt/venvs/mongo_source/bin:/opt/go/bin:${PATH}"
ENV GOPATH="/opt/go"

RUN apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq software-properties-common && \
    add-apt-repository ppa:longsleep/golang-backports && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
                                           golang-go git sudo iptables-persistent iproute2 \
                                           python3 python3-dev python3-venv && \
    mkdir -p /opt/go/bin && \
    go get github.com/tylertreat/comcast && \
    mkdir -p /opt/venvs/mongo_source && \
    mkdir -p /opt/venvs/mongo_source/scripts && \
    python3 -m venv /opt/venvs/mongo_source && \
    pip3 install -U pip wheel && \
    pip3 install pymongo==3.5.1 Faker && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache

COPY write_profile_data.py /opt/venvs/mongo_source/scripts/
COPY write_profile_data.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/write_profile_data.sh
CMD /usr/local/bin/write_profile_data.sh

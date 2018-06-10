FROM confluentinc/cp-kafka-connect:4.0.0-3
MAINTAINER Job Evers-Meltzer

# The amount of kruft that maven pulls in is impressive
# and makes this container massive.
# TODO: find a way to reduce this
RUN apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq maven && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Build the connector
ADD kafka-connect-mongodb /src
RUN cd /src && \
    mvn package && \
    mkdir -p /usr/share/java/confluent-common && \
    cp target/connect-mongodb-1.1-jar-with-dependencies.jar /usr/share/java/confluent-common && \
    mvn clean

FROM confluentinc/cp-kafka-connect:4.0.0-3
MAINTAINER Job Evers-Meltzer

COPY --from=0 /usr/share/java/confluent-common/connect-mongodb-1.1-jar-with-dependencies.jar /usr/share/java/confluent-common/connect-mongodb-1.1-jar-with-dependencies.jar

# Add in the configuration files
ADD connector.properties /etc/connect/
ADD worker.properties /etc/connect/
ADD connect-log4j.properties /etc/kafka/
ADD connect.sh /usr/local/bin/connect.sh
RUN chmod +x /usr/local/bin/connect.sh
RUN mkdir -p /var/lib/kafka-connect/

CMD /usr/local/bin/connect.sh
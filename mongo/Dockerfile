FROM mongo:3.4.14
MAINTAINER Job Evers-Meltzer

COPY my-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/my-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/my-entrypoint.sh"]
CMD ["mongod", "--replSet", "rs0"]

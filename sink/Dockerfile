FROM python:3-alpine

RUN pip install -U pip && pip install kafka

WORKDIR /root
COPY read_kafka.py .
CMD python3 /root/read_kafka.py

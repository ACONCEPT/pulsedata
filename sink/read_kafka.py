import json
import logging
import sys
import time
import os
import kafka

DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"
def main():
    logging.basicConfig(level="INFO", format=DEFAULT_FORMAT, filename = "/output/kafka_consumer_log.txt")
    consumer = get_consumer()
    consumer.subscribe(['mongo_pulsedata_profiles'])
    print(os.listdir("./"))
    consumer_start = time.time()
    while True:
        for record in consumer:
            message = json.loads(record.value.decode('utf-8'))
            payload = message['payload']
            profile_raw = payload['object']
            profile = json.loads(profile_raw)


def get_consumer():
    while True:
        try:
            consumer = kafka.KafkaConsumer(
                bootstrap_servers='kafka:9092', auto_offset_reset='earliest',
                consumer_timeout_ms=1000)
            return consumer
        except kafka.errors.NoBrokersAvailable:
            #logging.info('Waiting for kafka broker')
            time.sleep(1)


if __name__ == '__main__':
    sys.exit(main())

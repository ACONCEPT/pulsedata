import datetime
import logging
import random
import sys
import time

import faker
import pymongo


DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"

def main():
    logging.basicConfig(level="DEBUG", format=DEFAULT_FORMAT,filename = "/output/profile_write_log.txt")
    # need the timeouts otherwise with a poor network, we get stuck waiting a long time
    conn = pymongo.MongoClient(
        'mongo',
        replicaset='rs0', w=1, wtimeout=50,
        socketTimeoutMS=1000, connectTimeoutMS=1000,
        serverSelectionTimeoutMS=1000)
    wait_until_master(conn)
    fake = Fake(faker.Faker())
    for next_time in poisson_process(30):
        sleep_until(next_time)
        profile = fake.new_profile()
        insert(conn, profile)
        print("writing {}".format(profile['user_id']))
        logging.info('[!!]profile : {}'.format(profile['user_id']))

def wait_until_master(conn):
    while True:
        try:
            conn.admin.command('ismaster')
            logging.info('Node is master, moving forward')
            return
        except pymongo.errors.AutoReconnect:
            logging.warn('Waiting until we are master')
            time.sleep(1)


def poisson_process(lambd):
    now = time.time()
    while True:
        yield now
        delta = random.expovariate(lambd)
        now += delta

def sleep_until(next_time):
    now = time.time()
    if next_time > now:
        time.sleep(next_time - now)

class Fake(object):
    def __init__(self, fake):
        self.fake = fake
        self.count = 0

    def new_profile(self):
        self.count += 1
        return {
            'user_id': self.count,
            'name': self.fake.name(),
            'email': self.fake.email(),
            'creation_ts': datetime.datetime.now()
        }


def insert(conn, profile):
    while True:
        try:
            conn.pulsedata.profiles.insert_one(profile)
            return
        except pymongo.errors.NetworkTimeout:
            del profile['_id']
            continue


if __name__ == '__main__':
    sys.exit(main())

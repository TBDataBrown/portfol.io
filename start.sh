#!/usr/bin/env bash
set -xe

mkdir -p /var/log;
chmod -R 777 /var/log;
mongod --fork --logpath=/var/log/mongodb.log;
python3 data_acquire_test.py & python3 app.py;
#python3 -c 'import pymongo;list(pymongo.MongoClient().get_database("energy").energy.find())';

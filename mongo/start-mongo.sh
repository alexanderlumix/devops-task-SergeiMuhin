#!/bin/bash
set -e

KEYFILE=/etc/mongo-keyfile

USERNAME="${MONGO_INITDB_ROOT_USERNAME:-admin}"
PASSWORD="${MONGO_INITDB_ROOT_PASSWORD:-Unix1!forever}"

echo "Starting on port: $MONGO_PORT"
chmod 400 "$KEYFILE"

# Start mongod WITHOUT auth to create the initial user
mongod --port "$MONGO_PORT" --keyFile "$KEYFILE" --bind_ip_all --fork --logpath /tmp/mongod-init.log

# Wait until MongoDB is ready
until mongosh --port "$MONGO_PORT" --eval "db.adminCommand('ping')" &>/dev/null; do
  sleep 1
done

# Create the root user
mongosh --port "$MONGO_PORT" --eval "
  db = db.getSiblingDB('admin');
  try {
    db.createUser({user: '$USERNAME', pwd: '$PASSWORD', roles: ['root']});
    print('Admin user created.');
  } catch (e) {
    if (e.codeName === 'DuplicateKey') {
      print('Admin user already exists.');
    } else {
      throw e;
    }
  }
"

# Shutdown the temporary instance
mongod --port "$MONGO_PORT" --shutdown --dbpath /data/db

# Start with auth
exec mongod --port "$MONGO_PORT" --keyFile "$KEYFILE" --replSet rs0 --bind_ip_all --auth

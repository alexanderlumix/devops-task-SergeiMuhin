#!/bin/bash
mongosh --port "$MONGO_PORT" \
  -u "$MONGO_INITDB_ROOT_USERNAME" \
  -p "$MONGO_INITDB_ROOT_PASSWORD" \
  --authenticationDatabase admin \
  --quiet --eval 'rs.status()' > /dev/null
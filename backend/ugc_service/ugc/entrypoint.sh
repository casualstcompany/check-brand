#!/bin/bash

set -e

cmd="$*"

# DB
>&2 echo "Waiting for DB..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  >&2 echo "DB is unavailable - sleeping"
  sleep 2
done

>&2 echo "DB is up - executing command"

# REDIS
>&2 echo "Waiting for REDIS..."
# shellcheck disable=SC2086
until nc -z "$REDIS_HOST" $REDIS_PORT; do
  >&2 echo "REDIS is unavailable - sleeping"
  sleep 2
done

>&2 echo "REDIS is up - executing command"

# shellcheck disable=SC2086
exec $cmd

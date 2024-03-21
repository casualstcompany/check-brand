#!/bin/bash

set -e

cmd="$*"

>&2 echo "Waiting for BROKER..."
until nc -z $BROKER_HOST $BROKER_PORT; do
  >&2 echo "BROKER is unavailable - sleeping"
  sleep 2
done

>&2 echo "BROKER is up - executing command"

>&2 echo "Waiting for CACHE..."
until nc -z $CACHE_HOST $CACHE_PORT; do
  >&2 echo "Cache is unavailable - sleeping"
  sleep 2
done

>&2 echo "Cache is up - executing command"

exec $cmd

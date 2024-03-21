#!/bin/bash

set -e

cmd="$*"

# ES
>&2 echo "Waiting for ES..."
until nc -z "$ES_HOST" "$ES_PORT"; do
  >&2 echo "ES is unavailable - sleeping"
  sleep 4
done
>&2 echo "Waiting for ES... SSL"

until curl -s --cacert "$ES_PATH_CA_CRT" https://"$ES_HOST":"$ES_PORT" | grep -q "missing authentication credentials"; do
  >&2 echo "ES SSL is unavailable - sleeping"
  sleep 4
done

>&2 echo "ES is up - executing command"

# CACHE
>&2 echo "Waiting for CACHE..."
until nc -z $CACHE_HOST $CACHE_PORT; do
  >&2 echo "Cache is unavailable - sleeping"
  sleep 2
done

>&2 echo "Cache is up - executing command"


# shellcheck disable=SC2086
exec $cmd

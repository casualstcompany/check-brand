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

# ADMIN_DB
>&2 echo "Waiting for ADMIN_DB..."
until nc -z "$ADMIN_DB_HOST" "$ADMIN_DB_PORT"; do
  >&2 echo "ADMIN_DB is unavailable - sleeping"
  sleep 7
done

>&2 echo "ADMIN_DB is up - executing command"

# shellcheck disable=SC2086
exec $cmd

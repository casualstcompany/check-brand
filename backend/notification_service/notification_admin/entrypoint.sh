#!/bin/bash

set -e

cmd="$*"

>&2 echo "Waiting for DB..."
until nc -z $DB_HOST $DB_PORT; do
  >&2 echo "DB is unavailable - sleeping"
  sleep 2
done

>&2 echo "DB is up - executing command"

python manage.py migrate

if [ $SERVER_NAME != "ADMIN_GRPC" ]; then
  echo "start collectstatic"
  python manage.py collectstatic --noinput
fi

exec $cmd

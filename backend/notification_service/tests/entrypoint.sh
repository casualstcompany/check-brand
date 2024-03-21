#!/bin/bash

set -e

cmd="$*"

>&2 echo "Waiting for NOTIFICATION_API..."
until nc -z "$NOTIFICATION_API_HOST" "$NOTIFICATION_API_PORT"; do
  >&2 echo "NOTIFICATION_API is unavailable - sleeping"
  sleep 2
done

>&2 echo "NOTIFICATION_API is up - executing command"

exec $cmd

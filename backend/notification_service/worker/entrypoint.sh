#!/bin/bash

set -e

cmd="$*"

>&2 echo "Waiting for BROKER..."
until nc -z $BROKER_HOST $BROKER_PORT; do
  >&2 echo "BROKER is unavailable - sleeping"
  sleep 2
done

>&2 echo "BROKER is up - executing command"


>&2 echo "Waiting for ADMIN_GRPC..."
until nc -z $ADMIN_GRPC_HOST $ADMIN_GRPC_PORT; do
  >&2 echo "ADMIN_GRPC is unavailable - sleeping"
  sleep 2
done

>&2 echo "ADMIN_GRPC is up - executing command"

exec $cmd

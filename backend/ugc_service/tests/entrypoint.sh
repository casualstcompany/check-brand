#!/bin/bash

set -e

cmd="$*"

>&2 echo "Waiting for UGC..."
until nc -z $UGC_HOST $UGC_PORT; do
  >&2 echo "UGC is unavailable - sleeping"
  sleep 2
done

>&2 echo "UGC is up - executing command"

>&2 echo "Waiting for UGC_GRPC..."
until nc -z $UGC_GRPC_HOST $UGC_GRPC_PORT; do
  >&2 echo "UGC_GRPC is unavailable - sleeping"
  sleep 2
done

>&2 echo "UGC_GRPC is up - executing command"

>&2 echo "Waiting for AUTH..."
until nc -z $AUTH_HOST $AUTH_PORT; do
  >&2 echo "AUTH is unavailable - sleeping"
  sleep 2
done

>&2 echo "AUTH is up - executing command"

>&2 echo "Waiting for AUTH_GRPC..."
until nc -z $AUTH_GRPC_HOST $AUTH_GRPC_PORT; do
  >&2 echo "AUTH_GRPC is unavailable - sleeping"
  sleep 2
done

>&2 echo "AUTH_GRPC is up - executing command"

exec $cmd

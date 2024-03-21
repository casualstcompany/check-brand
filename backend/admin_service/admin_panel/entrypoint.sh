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
until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
  >&2 echo "REDIS is unavailable - sleeping"
  sleep 2
done

>&2 echo "REDIS is up - executing command"

if [ "$LOCAL_RUN" == "True" ]; then
  >&2 echo "Generate Protobufs for Local Volune - generate..."
  python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/auth_by_grpc/protobufs/auth_grpc.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grps_clients/ugc/protobufs/ugc_grpc.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grps_clients/notification/protobufs/notification_api.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/nft_tokens/grpc/nft_tokens.proto

  >&2 echo "Generate Protobufs for Local Volune - success"
fi

python manage.py migrate

if [ "$SERVER_NAME" == "admin_panel" ]; then
  python manage.py collectstatic --noinput
fi

exec $cmd

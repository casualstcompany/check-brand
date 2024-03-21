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
  cd app
  python -m grpc_tools.protoc -I ../app --python_out=. --grpc_python_out=. ../app/components/protobufs/auth_grpc.proto &&  \
    python -m grpc_tools.protoc -I ../app --python_out=. --grpc_python_out=. ../app/components/protobufs/nft_tokens.proto
  cd ..
  >&2 echo "Generate Protobufs for Local Volune - success"
fi


>&2 echo "Проверка миграций и обновление при необходимости"

flask db upgrade

>&2 echo "Запуск проекта"

# shellcheck disable=SC2086
exec $cmd

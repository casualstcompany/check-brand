FROM python:3.10-slim

ENV HOME_DIR=/usr/notification_api
ENV LOCAL_DIR=notification_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $HOME_DIR


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    apt install -y netcat-openbsd

COPY $LOCAL_DIR/requirements.txt .
RUN pip install -r requirements.txt

COPY $LOCAL_DIR/src ./src
COPY protobufs/notification_api.proto ./src/components/grpc/protobufs/notification_api.proto

COPY $LOCAL_DIR/entrypoint.sh .

WORKDIR $HOME_DIR/src

RUN python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/components/grpc/protobufs/notification_api.proto && \
    chmod +x ../entrypoint.sh

ENTRYPOINT [ "../entrypoint.sh" ]

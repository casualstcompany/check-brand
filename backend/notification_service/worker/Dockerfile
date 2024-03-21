FROM python:3.10-slim

ENV HOME_DIR=/usr/worker
ENV LOCAL_DIR=worker

WORKDIR $HOME_DIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    apt install -y netcat-openbsd

COPY $LOCAL_DIR/requirements.txt .
RUN pip install -r requirements.txt

COPY $LOCAL_DIR/src ./src
COPY $LOCAL_DIR/entrypoint.sh .
COPY protobufs/notification.proto ./src/components/protobufs/notification.proto

WORKDIR $HOME_DIR/src

RUN python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/components/protobufs/notification.proto && \
    chmod +x ../entrypoint.sh

ENTRYPOINT [ "../entrypoint.sh" ]

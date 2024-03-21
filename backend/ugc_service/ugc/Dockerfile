FROM python:3.10-slim

ENV HOME_DIR=/usr/ugc
ENV LOCAL_DIR=ugc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $HOME_DIR

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    apt install -y netcat-openbsd

COPY $LOCAL_DIR/requirements.txt .
COPY $LOCAL_DIR/dev_requirements.txt .
RUN pip install -r dev_requirements.txt

COPY $LOCAL_DIR/src ./src
COPY $LOCAL_DIR/entrypoint.sh .
COPY protobufs/ ./src/grpc_components/protobufs/

WORKDIR $HOME_DIR/src

RUN python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grpc_components/protobufs/auth_grpc.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grpc_components/protobufs/ugc_grpc.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grpc_components/protobufs/notification_api.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grpc_components/protobufs/nft_tokens.proto && \
    chmod +x ../entrypoint.sh

ENTRYPOINT [ "../entrypoint.sh" ]

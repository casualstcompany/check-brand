FROM python:3.11.4-slim

ENV HOME_DIR=/usr/admin_panel
ENV LOCAL_DIR=backend/admin_service/admin_panel

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
COPY $LOCAL_DIR/entrypoint.sh .
COPY protobufs/auth_grpc.proto ./src/auth_by_grpc/protobufs/auth_grpc.proto
COPY protobufs/ugc_grpc.proto ./src/grps_clients/ugc/protobufs/ugc_grpc.proto
COPY protobufs/notification_api.proto ./src/grps_clients/notification/protobufs/notification_api.proto
COPY protobufs/nft_tokens.proto ./src/nft_tokens/grpc/nft_tokens.proto

WORKDIR $HOME_DIR/src

RUN python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/auth_by_grpc/protobufs/auth_grpc.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grps_clients/ugc/protobufs/ugc_grpc.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grps_clients/notification/protobufs/notification_api.proto && \
    python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/nft_tokens/grpc/nft_tokens.proto && \
    chmod +x ../entrypoint.sh

ENTRYPOINT [ "../entrypoint.sh" ]

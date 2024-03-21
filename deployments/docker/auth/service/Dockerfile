FROM python:3.11.4-slim

ENV HOME_DIR=/usr/auth
ENV LOCAL_DIR=backend/auth_service/auth

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $HOME_DIR

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get install -y git && \
    pip install --upgrade pip && \
    apt install -y netcat-openbsd

COPY $LOCAL_DIR/requirements.txt .

RUN pip install -r requirements.txt && \
    pip install git+https://github.com/maxcountryman/flask-login.git#egg=flask-login

COPY $LOCAL_DIR/src ./src
COPY $LOCAL_DIR/entrypoint.sh .
COPY ["protobufs/auth_grpc.proto", "protobufs/nft_tokens.proto", "./src/app/components/protobufs/"]

WORKDIR $HOME_DIR/src/app

RUN python -m grpc_tools.protoc -I ../app --python_out=. --grpc_python_out=. ../app/components/protobufs/auth_grpc.proto &&  \
    python -m grpc_tools.protoc -I ../app --python_out=. --grpc_python_out=. ../app/components/protobufs/nft_tokens.proto &&  \
    chmod +x ../../entrypoint.sh

WORKDIR $HOME_DIR/src
ENTRYPOINT [ "../entrypoint.sh" ]

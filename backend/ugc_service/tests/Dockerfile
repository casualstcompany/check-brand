FROM python:3.10-slim

ENV HOME_DIR=/usr/tests
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $HOME_DIR

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    apt install -y netcat

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY ./functional ./functional

RUN python -m grpc_tools.protoc -I ../tests --python_out=. --grpc_python_out=. ../tests/functional/protobufs/ugc_grpc.proto
RUN python -m grpc_tools.protoc -I ../tests --python_out=. --grpc_python_out=. ../tests/functional/protobufs/auth_grpc.proto

WORKDIR $HOME_DIR/functional

RUN chmod +x ../entrypoint.sh
ENTRYPOINT [ "../entrypoint.sh"]

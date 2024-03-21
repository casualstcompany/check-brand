FROM python:3.11.4-slim

ENV HOME_DIR=/usr/etl
ENV LOCAL_DIR=backend/handler_service/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $HOME_DIR

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    apt install -y netcat-openbsd && \
    apt-get -y install curl

COPY $LOCAL_DIR/requirements.txt .
RUN pip install -r requirements.txt

COPY $LOCAL_DIR/src ./src
COPY $LOCAL_DIR/entrypoint.sh .

WORKDIR $HOME_DIR/src

RUN chmod +x ../entrypoint.sh

ENTRYPOINT [ "../entrypoint.sh" ]

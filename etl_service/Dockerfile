# syntax=docker/dockerfile:1

FROM python:3.8-slim

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt --no-cache-dir

COPY ./app /app/

WORKDIR /app

ADD docker_entrypoint.sh /docker_entrypoint.sh

RUN chmod +x /docker_entrypoint.sh

CMD ["/docker_entrypoint.sh"]
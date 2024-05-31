FROM python:3.10-slim

ENV LANG="C.UTF-8"

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg

COPY ./requirements.txt /tmp/requirements.txt

RUN python -m pip install -U --no-cache-dir pip && pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
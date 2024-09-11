FROM python:3.8-slim

ENV LANG="C.UTF-8"

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
FROM python:3.9.10-slim-buster as builder
RUN apt-get update \
    && apt-get -y install build-essential libpcre3-dev \
    && apt-get clean

COPY poetry.lock /build/
COPY pyproject.toml /build/
WORKDIR /build/
RUN pip install poetry && poetry export -o requirements.txt && pip install -r requirements.txt


FROM python:3.9.10-slim-buster as app
WORKDIR /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY . .
ENTRYPOINT uwsgi --ini docker/uwsgi.ini --http :$PORT

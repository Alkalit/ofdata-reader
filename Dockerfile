FROM python:3.11-slim-buster

RUN mkdir -p /src /db
COPY pyproject.toml /
COPY src/ /src/
RUN pip install --disable-pip-version-check  -e /

WORKDIR /src

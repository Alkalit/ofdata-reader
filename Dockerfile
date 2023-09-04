FROM python:3.11-slim-buster

RUN mkdir -p /src /db /configs
COPY pyproject.toml /
RUN pip install --disable-pip-version-check  -e /

WORKDIR /src
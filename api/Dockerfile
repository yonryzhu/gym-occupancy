FROM python:3.9.7-slim-bullseye

RUN apt-get update \
    && apt-get upgrade -y

RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

RUN adduser --disabled-password user
USER user

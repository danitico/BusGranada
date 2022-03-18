FROM python:3.9.9-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /bot
WORKDIR /bot
COPY . /bot

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

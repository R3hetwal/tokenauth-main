FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app


# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential


COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt




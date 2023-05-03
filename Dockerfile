FROM naxa/python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# RUN apt-get update && apt-get install -y lsb-release wget gnupg


# # Add PostgreSQL 15 repository
# RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
#     && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# # Update package lists and install PostgreSQL 15
# RUN apt-get update \
#     && apt-get install -y postgresql-15

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential && apt-get install -y postgis


COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt


# RUN apt-get update && apt-get install -y postgis


FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y apt-utils python-dev netcat gcc musl-dev python3-dev python3-pip python3-venv python3-wheel build-essential libpq-dev python3-psycopg2
RUN pip install --upgrade pip

RUN mkdir /code
RUN mkdir /opt/api
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /code/entrypoint.sh
COPY . /code/

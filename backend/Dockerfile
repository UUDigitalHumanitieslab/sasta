FROM python:3.6

# git to be able to install requirements from git
RUN apt-get update && apt-get install git && rm -rf /var/lib/apt/lists/*

# dependencies
RUN apt-get update && apt-get install -y libfolia-dev libxml2-dev

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip3 install cython
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]

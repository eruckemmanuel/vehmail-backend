# pull the official base image
FROM python:3.9.0

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python3-dev \
                       python3-cairo \
                       build-essential \
                       xmlsec1 \
                       libxmlsec1-dev \
                       pkg-config


# install dependencies
RUN pip install --upgrade pip

COPY ./app/requirements.txt ./

RUN pip install -r requirements.txt

# copy project
COPY ./app .

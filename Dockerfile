FROM ubuntu:16.04

RUN adduser --quiet --disabled-password qtuser

RUN apt-get update
RUN apt-get install -y \
	python3-pip \
	python3-pyqt5

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY src/ /app
WORKDIR /app


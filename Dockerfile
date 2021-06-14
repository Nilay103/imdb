FROM python:3
ENV PYTHONBUFFERED 1
RUN apt-get update -y && apt-get install -y python-pip python-dev
WORKDIR /fynd_app
ADD . /fynd_app
COPY ./requirements.txt /fynd_app/requirements.txt
RUN pip install -r requirements.txt
COPY . /fynd_app

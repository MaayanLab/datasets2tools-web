FROM ubuntu:14.04

MAINTAINER Denis Torre <denis.torre@mssm.com>

RUN apt-get update && apt-get install -y python
RUN apt-get update && apt-get install -y python-pip
RUN apt-get update && apt-get install -y python-dev
RUN apt-get update && apt-get install -y python-MySQLdb

RUN pip install numpy==1.12.1
RUN pip install pandas==0.19.2
RUN pip install Flask==0.12.1
RUN pip install sqlalchemy==1.1.9
RUN pip install flask-sqlalchemy==2.2

RUN mkdir datasets2tools
COPY . /datasets2tools

ENTRYPOINT python /datasets2tools/flask/__init__.py
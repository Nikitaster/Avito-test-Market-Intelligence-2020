FROM python:3.8
LABEL author="Nikita Gudkov nikitaster2001@gmail.com"

# запрет для python на создание файлов *.pyc
ENV PYTHONDONTWRITEBYTECODE 1

# запрет на буферизацию вывода в консоль для python
ENV PYTHONUNBUFFERED 1

#RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# fix executable for widnows
COPY ./docker-entrypoint.sh .
RUN apt-get update && \
    apt-get install -y dos2unix
RUN dos2unix ./docker-entrypoint.sh

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt



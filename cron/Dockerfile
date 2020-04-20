FROM python:3.7

ENV TZ=Europe/Moscow

RUN apt-get update && apt-get install -y cron

ADD config/requirements.txt /etc/requirements.txt
RUN pip install -r /etc/requirements.txt

ADD ./config/crontab /etc/cron.d/crontab

ADD src /src
WORKDIR /src

ENTRYPOINT cron -f
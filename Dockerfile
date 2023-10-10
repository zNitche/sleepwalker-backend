from python:3.10-slim

COPY . /sleepwalker
WORKDIR /sleepwalker

RUN apt update && apt -y install nano curl
RUN pip3 install -r requirements.txt

RUN chmod +x scripts/entrypoint.sh
RUN chmod +x scripts/celery_entrypoint.sh

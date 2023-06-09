# changed from slim
FROM python:3.9-slim

RUN apt-get update && apt-get -y install \
    build-essential libpq-dev ffmpeg libsm6 libxext6 wget

WORKDIR /opt
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 8500

ENTRYPOINT [ "bash", "start.sh" ]

FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y build-essential curl git make
COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt 
RUN mkdir -p /app
COPY . /app
WORKDIR /app

EXPOSE 8000
ENTRYPOINT ["tail", "-f", "/dev/null"]

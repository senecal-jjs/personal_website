FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# os tools
RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         gcc \
         libffi-dev \
         libssl-dev \ 
         libxslt-dev \
         bash \
         cmake \
         git \
         curl \
         vim \
         ca-certificates \
         libjpeg-dev \
         python3-dev \
         cargo \
         python3-pip \
         libpng-dev &&\
rm -rf /var/lib/apt/lists/*

RUN groupadd -r sitemanager && useradd -r -g sitemanager sitemanager

WORKDIR /home/website-v3 

# install requirements.txt 
COPY requirements.txt requirements.txt 
RUN pip3 install --upgrade setuptools 
RUN pip3 install -r requirements.txt

COPY app app 
COPY webapp.py config.py ./ 

ENV FLASK_APP webapp.py 

RUN chown -R sitemanager:sitemanager ./
USER sitemanager 

EXPOSE 5000 
ENTRYPOINT ["gunicorn", "--bind", ":8000", "webapp:app", "--reload", "--workers", "4"]
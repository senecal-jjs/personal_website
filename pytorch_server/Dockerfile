FROM bitnami/pytorch:1.12.1-debian-11-r23

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         gcc \
         libffi-dev \
         libssl-dev \ 
         libxslt-dev \
         bash \
         cmake \
         ca-certificates \
         libjpeg-dev \
         libpng-dev &&\
rm -rf /var/lib/apt/lists/*

WORKDIR /home/pytorch_server
COPY ps /home/pytorch_server

ENV REDIS_HOST 'redis'
ENV REDIS_PORT 6379 

# install requirements.txt 
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run_pytorch_server.py"]

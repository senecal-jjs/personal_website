FROM ubuntu:18.04

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
         wget \
         libpng-dev &&\
rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# No CUDA-specific steps
ENV NO_CUDA=1
RUN conda install -y pytorch-cpu torchvision-cpu -c pytorch \
 && conda clean -ya

RUN groupadd -r sitemanager && useradd -r -g sitemanager sitemanager

WORKDIR /home/pytorch_server
COPY ps /home/pytorch_server

ENV REDIS_HOST 'redis'
ENV REDIS_PORT 6379 

# install requirements.txt 
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run_pytorch_server.py"]
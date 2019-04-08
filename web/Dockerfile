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
         libpng-dev &&\
rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# check python version
RUN python --version 

# No CUDA-specific steps
ENV NO_CUDA=1
RUN conda install -y pytorch-cpu torchvision-cpu -c pytorch \
 && conda clean -ya

# Install HDF5 Python bindings
# RUN conda install -y h5py=2.8.0 \
#  && conda clean -ya
# RUN pip install --upgrade pip 
# RUN pip install h5py-cache==1.0

# # Install Graphviz
# RUN conda install -y graphviz=2.38.0 \
#  && conda clean -ya
# RUN pip install graphviz==0.8.4

# Install OpenCV3 Python bindings
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgtk2.0-0 \
#     libcanberra-gtk-module \
#  && rm -rf /var/lib/apt/lists/*
# RUN conda install -y -c menpo opencv3=3.1.0 \
# && conda clean -ya

RUN groupadd -r sitemanager && useradd -r -g sitemanager sitemanager

WORKDIR /home/website-v3 

# install requirements.txt 
COPY requirements.txt requirements.txt 
RUN pip install --upgrade setuptools 
RUN pip install -r requirements.txt
RUN pip install gunicorn 

COPY app app 
COPY webapp.py config.py boot.sh ./ 
RUN chmod +x boot.sh 

ENV FLASK_APP webapp.py 
ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD testpassword123
ENV POSTGRES_HOST postgres
ENV POSTGRES_PORT 5432
ENV POSTGRES_DB posts 

RUN chown -R sitemanager:sitemanager ./
USER sitemanager 

EXPOSE 5000 
ENTRYPOINT ["./boot.sh"]
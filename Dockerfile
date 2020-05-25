# Build an image that can do training and inference in SageMaker
# This is a Python 2 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM ubuntu:16.04

MAINTAINER Amazon AI <sage-learner@amazon.com>

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
	 python3.5 \
         libgcc-5-dev \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Here we get all python packages.
# There's substantial overlap between scipy and numpy that we eliminate by
# linking them together. Likewise, pip leaves the install caches populated which uses
# a significant amount of space. These optimizations save a fair amount of space in the
# image, which reduces start up time.
RUN wget https://bootstrap.pypa.io/3.3/get-pip.py 
RUN pip install --upgrade pip

COPY "requirements.txt" .
RUN ["pip", "install", "-r", "requirements.txt"]


ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY linear_svm /opt/program
WORKDIR /opt/program


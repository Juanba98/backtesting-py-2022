# Use Python 3.12 on Debian Bullseye as the base image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Set the working directory inside the container
WORKDIR /workspace

# Update the package list and install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && rm -rf /workspace/ta-lib-0.4.0-src.tar.gz /workspace/ta-lib/ 

RUN python -m pip install --upgrade pip
#EXIT with 1 run manually
#RUN pip install --no-cache-dir -r /workspace/requirements.txt
# Copy the source code into the container
COPY . /workspace


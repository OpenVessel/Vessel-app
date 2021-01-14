# Use Python 3.7.2 container image
## Conttainer base on Ubuntu 
#
#
## CMake, VTK, 
#
#FROM python:3.7.2-stretch
FROM ubuntu:18.04

#MAINTANER Leslie Wubbel "lesliemwubbel@gmail.com"

RUN apt-get update \
&& apt-get install -y build-essential \
&& apt-get install -y git \
&& apt-get install -y cmake \
&& apt-get install -y mesa-common-dev \
&& apt-get install -y mesa-utils \
&& apt-get install -y freeglut3-dev
RUN apt-get install -y python3-pip python3-dev 
RUN apt-get install -y wget
RUN cd /usr/local/bin 
RUN ln -s /usr/bin/python3 python 
RUN pip3 install --upgrade pip 
RUN apt-get install -y nodejs 
RUN node --version 

## the c++ code collection
  ## Cmake
  ## VTK
  ## GDCM 

### Cmake installation on Ubuntu 18.04
RUN mkdir /C_code
WORKDIR /C_code \
&& wget -q https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3.tar.gz \
&& tar -zxf cmake-3.17.3.tar.gz \ 
&& cd cmake-3.17.3 \
&& make \
&& cmake --version


## Building VTK on Ubuntu 18.04
WORKDIR /C_code \
git clone --recursive https://gitlab.kitware.com/vtk/vtk.git
RUN mkdir -p vtk/build
RUN cd vtk/build
RUN cmake ../ -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=ON -DCMAKE_BUILD_TYPE=Release -DVTK_WRAP_PYTHON=ON
RUN make -j
RUN make install
RUN cmake ../ -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=ON -DCMAKE_BUILD_TYPE=Release -DVTK_WRAP_PYTHON=ON



#Set the working directory to /vessel_app
WORKDIR /Back-end
## Setting up JavaScript/EMCAScript
RUN cd Back-end\vessel_app\static
RUN npm install 
RUN npm build
RUN npm watch

# Copy the current directory contents into the container at /vessel_app
ADD . /Back-end

## Install the  dependencies
RUN pip3 install -r requirements.txt 
RUN cd Vessel-app/vessel_app/Back-end

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

## Celery app 
RUN celery -A vessel_app.file_pipeline.celery_tasks.celery worker --loglevel=info -P gevent

### Supervisord script!


## run the command to start uWSGI

CMD ["uwsgi", "app.ini"]
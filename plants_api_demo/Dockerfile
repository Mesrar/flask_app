FROM python:3.8.5
ADD . /rest_api_demo
WORKDIR /rest_api_demo
RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
RUN pip3 install -r requirements.txt
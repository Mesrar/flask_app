FROM python:3.8.5

COPY rest_api_demo/app.py /app/app.py
COPY rest_api_demo/settings.py /app/settings.py
COPY rest_api_demo/logging.conf /app/logging.conf

COPY rest_api_demo/api /app/api
COPY rest_api_demo/api/* /app/api/

COPY rest_api_demo/data /app/data
COPY rest_api_demo/data/* /app/data/

COPY rest_api_demo/static /app/static
COPY rest_api_demo/static/manifest.json /app/static/manifest.json
COPY rest_api_demo/static/swagger.json /app/static/swagger.json
COPY rest_api_demo/static/robots.txt /app/static/robots.txt
COPY rest_api_demo/static/logo192.png /app/static/logo192.png
COPY rest_api_demo/static/logo512.png /app/static/logo512.png
COPY rest_api_demo/static/index.html /app/static/index.html
COPY rest_api_demo/static/favicon.ico /app/static/favicon.ico
COPY rest_api_demo/static/asset-manifest.json /app/static/asset-manifest.json

COPY rest_api_demo/static/static /app/static/static
COPY rest_api_demo/static/static/css/* /app/static/static/css/
COPY rest_api_demo/static/static/js/* /app/static/static/js/
COPY rest_api_demo/static/static/media/* /app/static/static/media/

COPY requirements.txt /app/requirements.txt

RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN pip3 install -r /app/requirements.txt

WORKDIR /app

EXPOSE 5000
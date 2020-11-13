RUN apt-get update -y

FROM python:3.8.5
ADD . /rest_api_demo
WORKDIR /rest_api_demo
RUN apt-get install gunicorn3 -y

COPY requirements.txt requirements.txt
COPY flaskapp /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/
FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY flaskapp.conf /etc/nginx/conf.d/

CMD ["gunicorn3", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]
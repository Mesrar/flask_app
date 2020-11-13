RUN apt-get update -y
FROM python:3.8.5
ADD . /rest_api_demo
WORKDIR /rest_api_demo
RUN pip3 install -r requirements.txt

FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY flaskapp.conf /etc/nginx/conf.d/
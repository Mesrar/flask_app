FROM python:3.8.5

COPY rest_api_demo/ /app
ENV APP /app

WORKDIR $APP

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .
COPY . .
RUN pip3 install -r requirements.txt

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]

# image=jenek46/backend:latest
FROM python:3.10.9-slim-buster

WORKDIR /backend

ENV TORNADO_APP=app.py

# ENV TORNADO_RUN_HOST 0.0.0.0
COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -U --no-cache-dir -r /tmp/requirements.txt

COPY *.py .

EXPOSE 8080

COPY ./app ./app

CMD python3 -u app.main
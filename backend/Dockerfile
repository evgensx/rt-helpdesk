# image=jenek46/backend:latest
FROM python:3.11.1-slim-buster

WORKDIR /app

# ENV TORNADO_RUN_HOST 0.0.0.0
COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -U --no-cache-dir -r /tmp/requirements.txt

COPY /app /app

EXPOSE 8888

CMD python3 -u main.py
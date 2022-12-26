# image=jenek46/backend:latest
FROM python:3.10.9-slim-buster
WORKDIR /backend
ENV TORNADO_APP=app.py
# ENV TORNADO_RUN_HOST 0.0.0.0
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt
COPY *.py .
EXPOSE 8080
CMD python3 -u app:ma
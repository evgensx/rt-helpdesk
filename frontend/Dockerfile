# image=jenek46/backend:latest
FROM python:3.10.9-slim-buster
WORKDIR /frontend
ENV RUN_APP=app.py
# ENV TORNADO_RUN_HOST=0.0.0.0
COPY *.html .
COPY *.css .
COPY *.js .
COPY *.py .
EXPOSE 80
CMD python3 -u $RUN_APP
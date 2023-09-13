FROM python:3.8-slim

RUN pip install Flask requests

COPY . /app
WORKDIR /app


CMD ["python", "proxy.py"]

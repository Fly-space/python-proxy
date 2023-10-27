FROM python:3.8-slim

RUN pip install Flask gunicorn requests

COPY . /app
WORKDIR /app

ENV FLASK_APP=proxy:app

CMD ["gunicorn", "-b", "0.0.0.0:80", "proxy:app"]

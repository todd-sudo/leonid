ARG PYTHON_VERSION=3.9-slim-bullseye

FROM python:${PYTHON_VERSION} as python

COPY . .

RUN pip install -r requirements.txt

ARG APP_HOME=/app

# RUN ["python", "main.py"]
FROM python:3.11.1-alpine

RUN apk update

RUN pip install --upgrade pip
RUN pip install -U setuptools pip

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD bin/boot.sh
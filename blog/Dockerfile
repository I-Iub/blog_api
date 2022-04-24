FROM python:3.8-slim

WORKDIR /blog_api

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

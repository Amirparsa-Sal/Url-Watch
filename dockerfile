FROM python:3.9-alpine

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

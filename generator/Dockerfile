FROM python:3.6.9-alpine3.10

RUN apk add --no-cache build-base libffi-dev openssl libressl-dev musl-dev bash
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY ./wait-for-it.sh /app/wait-for-it.sh
COPY ./generator /app
CMD python3 generator.py

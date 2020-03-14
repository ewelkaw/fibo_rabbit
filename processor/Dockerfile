FROM python:3.6.9-alpine3.10

RUN apk add --no-cache build-base libffi-dev openssl libressl-dev musl-dev bash
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 9000
COPY ./wait-for-it.sh /app/wait-for-it.sh
COPY ./db_connector.py /app/db_connector.py
COPY ./processor /app
CMD python3 processor.py
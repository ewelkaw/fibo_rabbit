FROM python:3.6.9-alpine3.10

RUN apk add --no-cache build-base libffi-dev openssl libressl-dev musl-dev bash
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
COPY ./wait-for-it.sh /app/wait-for-it.sh
COPY ./db_connector.py /app/db_connector.py
COPY ./api /app
ENV FLASK_ENV=development
ENV FLASK_APP=api.py
ENV FLASK_DEBUG=1
CMD flask run
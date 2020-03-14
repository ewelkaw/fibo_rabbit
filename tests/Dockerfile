FROM python:3.6.9-alpine3.10

RUN apk add --no-cache build-base libffi-dev openssl libressl-dev musl-dev bash
WORKDIR /tests
COPY ./tests/requirements-tests.txt /tests/requirements-tests.txt
RUN pip3 install -r requirements-tests.txt
COPY ./wait-for-it.sh /tests/wait-for-it.sh
COPY ./tests /tests
CMD python3 tests.py
docker build -t fibotest -f tests/Dockerfile .
docker run --network container:api fibotest /tests/wait-for-it.sh localhost:5000 -- python tests.py
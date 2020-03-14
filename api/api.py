import json
import pika
from flask import request, Flask, Response
from db_connector import DBConnector
import logging
import os

log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = Flask(__name__)
connector = DBConnector()


class RabbitConnector:
    def __init__(self, queue_name):
        self._queue_name = queue_name
        self.set_connector()

    def set_connector(self):
        host = os.getenv("RABBIT_HOST", "localhost")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        channel = connection.channel()

        channel.queue_declare(queue=self._queue_name)
        self._channel = channel

    def send(self, data, counter=0):
        try:
            self._channel.basic_publish(
                exchange="", routing_key=self._queue_name, body=data
            )
        except BrokenPipeError:
            counter = counter + 1
            if counter > 10:
                raise Exception("Can't re-connect to rabbit")
            self.set_connector()
            self.send(data, counter)


rabbit_connector = RabbitConnector("fibo_requests")


@app.route("/api/fibo/<int:number>", methods=["GET"])
def get_sequence(number):
    db_seq = connector.get_sequence(number)
    if db_seq is None:
        output = {
            "error": "Calculation have been not requested or have not been finished yet."
        }
        status = 404
    else:
        (number, sequence) = db_seq
        output = {"number": number, "sequence": json.loads(sequence)}
        status = 200

    return Response(
        json.dumps(output), headers={"Content-Type": "application/json"}, status=status,
    )


@app.route("/api/fibo", methods=["POST"])
def post_sequence():
    data = request.json
    number = data.get("number")
    if isinstance(number, int):
        sequence = connector.get_sequence(number)
        if not sequence:
            rabbit_connector.send(json.dumps({"number": number}))
            logger.info("Request has been sent to the queue")
            return Response(
                '{"success": "Request will be processed"}',
                headers={"Content-Type": "application/json"},
                status=202,
            )
        return Response(status=303, headers={"Location": f"/api/fibo/{number}"})
    else:
        return Response(
            '{"error": "Invalid number - you need to provide int"}',
            headers={"Content-Type": "application/json"},
            status=400,
        )


@app.route("/api/fibo", methods=["GET"])
def healthcheck():
    return Response(status=204)

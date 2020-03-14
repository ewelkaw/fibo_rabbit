from fibo_generator import fibo_gen
import pika
import json
import logging
import os

log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

host = os.getenv("RABBIT_HOST", "localhost")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue="fibo_requests")


def callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info(" [x] Generator received %r" % data)

    data["sequence"] = []
    for i in fibo_gen(data["number"]):
        data["sequence"].append(i)
    logger.info(" [x] Sequence generated")

    # sending response to the responses queue
    channel.queue_declare(queue="fibo_responses")
    channel.basic_publish(
        exchange="", routing_key="fibo_responses", body=json.dumps(data),
    )


channel.basic_consume(
    queue="fibo_requests", on_message_callback=callback, auto_ack=True
)

logger.info(" [*] Waiting for generation requests. To exit press CTRL+C")
channel.start_consuming()

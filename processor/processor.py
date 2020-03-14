import pika
import json
from db_connector import DBConnector
import logging
import os


log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

connector = DBConnector()

host = os.getenv("RABBIT_HOST", "localhost")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue="fibo_responses")


def callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info(" [x] Processor received %r" % data)
    connector.insert_sequence(int(data["number"]), json.dumps(data["sequence"]))
    logger.info(" [x] Sequence saved for %r" % data)


channel.basic_consume(
    queue="fibo_responses", on_message_callback=callback, auto_ack=True
)


logger.info(" [*] Waiting for generated fibos. To exit press CTRL+C")
channel.start_consuming()

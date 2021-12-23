#!/usr/bin/env python3
import logging
import pika
from .config import CONFIG

logging.basicConfig(level=logging.INFO)
# ^- TODO: Make this configurable

logger = logging.getLogger("worker.main")


def callback(channel, method, properties, body):
    channel.basic_ack(method.delivery_tag)

    job_id = body.decode("ascii")
    # TODO: Do the actual processing
    logger.info("Received job %s", job_id)


def main():
    logger.info("Connecting to message queue")
    connection = pika.BlockingConnection(pika.URLParameters(CONFIG.mq_url))

    logger.info("Creating message queue channel")
    channel = connection.channel()

    logger.info("Declaring queue")
    channel.queue_declare(queue=CONFIG.mq_queue)

    logger.info("Consuming from message queue")
    try:
        channel.basic_consume(queue=CONFIG.mq_queue, on_message_callback=callback)
        channel.start_consuming()
    finally:
        logger.info("Cancelling message queue channel")
        requeued_messages = channel.cancel()
        logger.info("Requeued %i messages", requeued_messages)
        connection.close()


if __name__ == '__main__':
    main()

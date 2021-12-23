#!/usr/bin/env python3
import logging
import pika
from . import crud
from .config import CONFIG
from .storage import InputFile, OutputFile
from .database import get_database

logging.basicConfig(level=logging.INFO)
# ^- TODO: Make this configurable

logger = logging.getLogger("ips.worker")


def callback(channel, method, properties, body):
    job_id = body.decode("ascii")
    logger.info("Received job %s", job_id)

    # Copy input file content to output file:
    with InputFile(job_id) as fi:
        with OutputFile() as fo:
            fo.copy_from_file(fi.file)

            output_uuid = fo.uuid
            logging.info("Created output file %s", output_uuid)
    # TODO: Do the actual processing

    # Update database entry:
    db = next(get_database())
    crud.finish_processing_job(db, job_id, output_uuid)

    # Acknowledge the message:
    channel.basic_ack(method.delivery_tag)
    logging.info("Acknowledged job %s", job_id)


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


if __name__ == "__main__":
    main()

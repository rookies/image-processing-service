#!/usr/bin/env python3
"""
This is the main file of the Image Processing Service worker processes.
"""
import logging
import pika
from PIL import Image, ImageFilter
from . import crud
from .config import CONFIG
from .storage import create_output_file, get_input_file_path
from .database import get_database
from .enums import ProcessingStatus

logger = logging.getLogger("ips.worker")


def callback(channel, method, _properties, body):
    """
    This function is called each time a job is received via the message queue.
    """
    job_id = body.decode("ascii")
    logger.info("Received job %s", job_id)

    # Get database connection:
    db = next(get_database())

    # Set status to PROCESSING:
    crud.update_processing_job_status(db, job_id, ProcessingStatus.PROCESSING)

    # Process the image:
    try:
        with Image.open(get_input_file_path(job_id)) as img:
            logger.info(
                "Opened file %s with format %s, size %s", job_id, img.format, img.size
            )
            img_out = img.filter(ImageFilter.BLUR)

            output_uuid, output_path = create_output_file()
            img_out.save(output_path, img.format)
            logger.info("Created output file %s", output_uuid)
    except OSError as exc:
        # Set status to FAILED:
        logger.warning("Processing of job %s failed: %s", job_id, exc)
        crud.update_processing_job_status(db, job_id, ProcessingStatus.FAILED)
    else:
        # Set status to FINISHED and add output UUID:
        crud.finish_processing_job(db, job_id, output_uuid)

    # Acknowledge the job:
    channel.basic_ack(method.delivery_tag)
    logger.info("Executed and acknowledged job %s", job_id)


def main():
    """
    This is the main entrypoint.
    """
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

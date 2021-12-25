#!/usr/bin/env python3
"""
This file provides access to the message queue.
"""
import uuid
import logging
import pika
from .config import CONFIG

logger = logging.getLogger("ips.queue")
MQConnection = pika.BlockingConnection


def get_queue():
    """
    Provides connections to the message queue.
    """
    mq = pika.BlockingConnection(pika.URLParameters(CONFIG.mq_url))
    try:
        yield mq
    finally:
        mq.close()


def publish_processing_job(mq: MQConnection, job_id: uuid.UUID):
    """
    Publishes a processing job to the given message queue.
    """
    channel = mq.channel()
    channel.queue_declare(queue=CONFIG.mq_queue)
    channel.basic_publish(
        exchange="", routing_key=CONFIG.mq_queue, body=bytes(str(job_id), "ascii")
    )

    logger.info("Published processing job %s to queue %s", job_id, CONFIG.mq_queue)

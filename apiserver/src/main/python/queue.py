#!/usr/bin/env python3
import uuid
import pika
from .config import CONFIG

MQConnection = pika.BlockingConnection


def get_queue():
    mq = pika.BlockingConnection(pika.URLParameters(CONFIG.mq_url))
    try:
        yield mq
    finally:
        mq.close()


def publish_processing_job(mq: MQConnection, job_id: uuid.UUID):
    channel = mq.channel()
    channel.basic_publish('', '', bytes(str(job_id), 'ascii'))

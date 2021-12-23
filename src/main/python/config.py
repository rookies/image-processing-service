#!/usr/bin/env python3
import os
import environ


@environ.config(prefix="IPS")
class Config:
    # Database URL:
    db_url = environ.var("postgresql://ips:ips@127.0.0.1/ips")
    # Message queue URL:
    mq_url = environ.var("amqp://guest:guest@127.0.0.1/%2F")
    # Message queue queue:
    mq_queue = environ.var("ips_processing_jobs")
    # File storage path:
    storage_path = environ.var("/tmp/ips_storage")

CONFIG = Config.from_environ(os.environ)
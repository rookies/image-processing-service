#!/usr/bin/env python3
import os
import logging
import environ
import attr.validators


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
    # Loglevel
    loglevel = environ.var(
        "INFO",
        validator=attr.validators.in_(
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        ),
    )


CONFIG = Config.from_environ(os.environ)

# Configure logging:
logging.basicConfig(level=getattr(logging, CONFIG.loglevel))

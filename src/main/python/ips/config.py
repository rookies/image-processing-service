#!/usr/bin/env python3
"""
This file reads the application configuration from environment variables. It also
configures the logging module.
"""
import os
import logging
import environ
import attr.validators


@environ.config(prefix="IPS")
class Config:
    """
    This is the main configuration class which defines the config options
    the application accepts.
    """

    # pylint: disable=too-few-public-methods

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


CONFIG = environ.to_config(Config, os.environ)

# Configure logging:
logging.basicConfig(level=getattr(logging, CONFIG.loglevel))

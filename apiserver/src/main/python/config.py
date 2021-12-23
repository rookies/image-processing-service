#!/usr/bin/env python3
import os
import environ


@environ.config(prefix="IPS_API")
class Config:
    # Database URL:
    db_url = environ.var("postgresql://ips:ips@127.0.0.1/ips")
    # MessageQueue URL:
    mq_url = environ.var("amqp://guest:guest@127.0.0.1/%2F")
    # File storage path:
    storage_path = environ.var("/tmp/ips_storage")

CONFIG = Config.from_environ(os.environ)

#!/usr/bin/env python3
import os
import environ


@environ.config(prefix="IPS_API")
class Config:
    db_url = environ.var("postgresql://postgres:password@127.0.0.1/postgres")
    storage_path = environ.var("/tmp/ips_storage")

CONFIG = Config.from_environ(os.environ)

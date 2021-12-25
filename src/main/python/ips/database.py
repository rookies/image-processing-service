#!/usr/bin/env python3
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import CONFIG

engine = create_engine(CONFIG.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

logger = logging.getLogger("ips.database")


def get_database():
    db = SessionLocal()
    try:
        logger.info("Returning database connection %s", db)
        yield db
    finally:
        db.close()
        logger.info("Closed database connection %s", db)

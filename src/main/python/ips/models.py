#!/usr/bin/env python3
"""
This file contains all database models as well as custom database column types.
"""
import uuid
from sqlalchemy import Column, Enum, Text
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from .enums import ProcessingStatus


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    See https://docs.sqlalchemy.org/en/14/core/custom_types.html
    """

    # pylint: disable=abstract-method

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())

        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return f"{uuid.UUID(value).int:032x}"

        return f"{value.int:032x}"

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value


class ProcessingJob(Base):
    """
    An image processing job. It is identified by a UUID generated at creation, has
    a processing status, the filename and content-type of the uploaded image, and
    (once the processing is finished) the UUID of the generated output file.
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "processing_jobs"

    uuid = Column(GUID, primary_key=True, index=True, default=uuid.uuid4)
    status = Column(
        Enum(ProcessingStatus), default=ProcessingStatus.WAITING, nullable=False
    )
    output_uuid = Column(GUID, nullable=True)
    original_filename = Column(Text, server_default="", nullable=False)
    original_content_type = Column(Text, server_default="", nullable=False)

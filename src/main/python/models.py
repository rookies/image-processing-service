#!/usr/bin/env python3
import uuid
from sqlalchemy import Column, Integer, Enum
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

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    uuid = Column(GUID, primary_key=True, index=True, default=uuid.uuid4)
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.WAITING)
    output_uuid = Column(GUID, nullable=True)

#!/usr/bin/env python3
"""
This file contains the schemas used for API requests and responses.
"""
import uuid
from pydantic import BaseModel
from .enums import ProcessingStatus


class ProcessingJobBase(BaseModel):
    """Base schema for an image processing job."""

    original_filename: str
    original_content_type: str


class ProcessingJobCreate(ProcessingJobBase):
    """Schema for creating an image processing job."""


class ProcessingJob(ProcessingJobBase):
    """Schema for returning an image processing job."""

    # pylint: disable=too-few-public-methods
    uuid: uuid.UUID
    status: ProcessingStatus

    class Config:
        """Configuration for the schema."""

        orm_mode = True

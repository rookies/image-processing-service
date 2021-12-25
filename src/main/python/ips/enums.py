#!/usr/bin/env python3
"""
This file contains enums used e.g. by database models.
"""
import enum


class ProcessingStatus(str, enum.Enum):
    """
    The processing status of an image processing job.
    """

    WAITING = "waiting"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"
    ABORTED = "aborted"

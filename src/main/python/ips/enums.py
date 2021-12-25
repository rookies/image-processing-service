#!/usr/bin/env python3
import enum


class ProcessingStatus(str, enum.Enum):
    WAITING = "waiting"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"
    ABORTED = "aborted"

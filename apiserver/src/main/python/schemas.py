#!/usr/bin/env python3
import uuid
from pydantic import BaseModel
from .enums import ProcessingStatus


class ProcessingJobBase(BaseModel):
    pass


class ProcessingJobCreate(ProcessingJobBase):
    pass


class ProcessingJob(ProcessingJobBase):
    uuid: uuid.UUID
    status: ProcessingStatus

    class Config:
        orm_mode = True

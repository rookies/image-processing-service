#!/usr/bin/env python3
import uuid
from sqlalchemy.orm import Session
from . import models, schemas
from .enums import ProcessingStatus


def get_processing_jobs(db: Session):
    return db.query(models.ProcessingJob).all()


def get_processing_job(db: Session, job_id: uuid.UUID):
    return db.query(models.ProcessingJob).filter(models.ProcessingJob.uuid == job_id).first()


def create_processing_job(db: Session, job: schemas.ProcessingJobCreate):
    db_job = models.ProcessingJob()
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


def finish_processing_job(db: Session, job_id: uuid.UUID, output_id: uuid.UUID):
    print(type(db))
    job = get_processing_job(db, job_id)
    if job is None:
        raise ValueError("No job with UUID %s" % job_id)

    job.output_uuid = output_id
    job.status = ProcessingStatus.FINISHED
    db.add(job)
    db.commit()

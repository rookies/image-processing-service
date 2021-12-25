#!/usr/bin/env python3
"""
This file implements create, read, update, and delete operations for database
objects.
"""
import uuid
from sqlalchemy.orm import Session
from . import models, schemas
from .enums import ProcessingStatus


def get_processing_jobs(db: Session):
    """
    Returns all processing jobs.
    """
    return db.query(models.ProcessingJob).all()


def get_processing_job(db: Session, job_id: uuid.UUID):
    """
    Returns the processing job with the given UUID.
    """
    return (
        db.query(models.ProcessingJob)
        .filter(models.ProcessingJob.uuid == job_id)
        .first()
    )


def create_processing_job(db: Session, job: schemas.ProcessingJobCreate):
    """
    Creates a processing job from the given schema.
    """
    db_job = models.ProcessingJob(
        original_filename=job.original_filename,
        original_content_type=job.original_content_type,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


def update_processing_job_status(
    db: Session, job_id: uuid.UUID, status: ProcessingStatus
):
    """
    Updates the status of the processing job with the given UUID to the given value.
    """
    job = get_processing_job(db, job_id)
    if job is None:
        raise ValueError(f"No job with UUID {job_id}")

    job.status = status
    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def finish_processing_job(db: Session, job_id: uuid.UUID, output_id: uuid.UUID):
    """
    Updates the status of the processing job with the given UUID to FINISHED and
    sets the output UUID to the given value.
    """
    job = get_processing_job(db, job_id)
    if job is None:
        raise ValueError(f"No job with UUID {job_id}")

    job.output_uuid = output_id
    job.status = ProcessingStatus.FINISHED
    db.add(job)
    db.commit()
    db.refresh(job)

    return job

#!/usr/bin/env python3
import uuid
import logging
from typing import List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .enums import ProcessingStatus
from .database import get_database, engine
from .storage import store_input_file, get_output_file_path
from .queue import MQConnection, get_queue, publish_processing_job

app = FastAPI(
    title="Image Processing Service",
    version="0.1.0",
)
logger = logging.getLogger("ips.main")


@app.post("/upload", response_model=schemas.ProcessingJob)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
    mq: MQConnection = Depends(get_queue),
):
    """
    Uploads an image and triggers the processing.
    """
    logger.info("File named '%s' (%s) uploaded", file.filename, file.content_type)

    # Create job in the database:
    job = crud.create_processing_job(
        db,
        schemas.ProcessingJobCreate(
            original_filename=file.filename, original_content_type=file.content_type
        ),
    )
    logger.info("Created database entry with UUID %s", job.uuid)

    # Store image on disk:
    await store_input_file(job.uuid, file)

    # Trigger processing via message queue:
    publish_processing_job(mq, job.uuid)

    return job


@app.get("/jobs/{job_id}/status", response_model=schemas.ProcessingJob)
async def get_job_status(job_id: uuid.UUID, db: Session = Depends(get_database)):
    """
    Returns the processing status of the job with the given ID.
    """
    job = crud.get_processing_job(db, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@app.get("/jobs/{job_id}/download")
async def download_result(job_id: uuid.UUID, db: Session = Depends(get_database)):
    """
    Provides the processed image for download.
    """
    job = crud.get_processing_job(db, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != ProcessingStatus.FINISHED:
        raise HTTPException(status_code=202, detail="Job not finished")

    return FileResponse(
        path=get_output_file_path(job.output_uuid),
        filename=job.original_filename,
        media_type=job.original_content_type,
    )


@app.get("/jobs", response_model=List[schemas.ProcessingJob])
async def list_jobs(db: Session = Depends(get_database)):
    """
    Lists all jobs.
    """
    return crud.get_processing_jobs(db)

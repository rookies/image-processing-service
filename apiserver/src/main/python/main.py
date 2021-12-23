#!/usr/bin/env python3
import uuid
import logging
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .enums import ProcessingStatus
from .database import SessionLocal, engine
from .storage import store_input_file

models.Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.DEBUG)
# ^- TODO: Make this configurable

app = FastAPI()
logger = logging.getLogger("apiserver.main")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload", response_model=schemas.ProcessingJob)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads an image and triggers the processing.
    """
    logger.info("File named '%s' (%s) uploaded", file.filename, file.content_type)

    # Create job in the database:
    job = crud.create_processing_job(db, schemas.ProcessingJobCreate())
    logger.info("Created database entry with UUID %s", job.uuid)

    # Store image on disk:
    await store_input_file(job.uuid, file)
    # TODO: Trigger processing via message queue
    return job


@app.get("/jobs/{job_id}/status", response_model=schemas.ProcessingJob)
async def get_job_status(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Returns the processing status of the job with the given ID.
    """
    job = crud.get_processing_job(db, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@app.get("/jobs/{job_id}/download")
async def download_result(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Provides the processed image for download.
    """
    job = crud.get_processing_job(db, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != ProcessingStatus.FINISHED:
        raise HTTPException(status_code=202, detail="Job not finished")

    # TODO: Return processed image
    return {}


@app.get("/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    """
    Lists all jobs.
    """
    return crud.get_processing_jobs(db)

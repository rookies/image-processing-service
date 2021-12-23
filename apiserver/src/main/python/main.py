#!/usr/bin/env python3
import uuid
from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
from .enums import ProcessingStatus
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
    # TODO
    return crud.create_processing_job(db, schemas.ProcessingJobCreate())


@app.get("/jobs/{job_id}/status")
async def get_job_status(job_id: uuid.UUID) -> dict:
    """
    Returns the processing status of the job with the given ID.
    """
    # TODO
    return {
        "job_id": job_id,
        "status": ProcessingStatus.WAITING,
    }


@app.get("/jobs/{job_id}/download")
async def download_result(job_id: uuid.UUID) -> dict:
    """
    Provides the processed image for download.
    """
    # TODO
    return {}


@app.get("/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    """
    Lists all jobs.
    """
    return crud.get_processing_jobs(db)

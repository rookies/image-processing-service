#!/usr/bin/env python3
import uuid
import enum
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


class ProcessingStatus(str, enum.Enum):
    WAITING = "waiting"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"
    ABORTED = "aborted"


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> dict:
    """
    Uploads an image and triggers the processing.
    """
    # TODO
    return {
        "filename": file.filename,
        "job_id": uuid.uuid4(),
    }


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

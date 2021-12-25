#!/usr/bin/env python3
"""
This file provides access to the file storage that is shared between API server
and workers.
"""
import uuid
import os.path
import logging
from typing import Tuple
from fastapi import UploadFile
from .config import CONFIG

INPUT_STORAGE_PATH = os.path.join(CONFIG.storage_path, "input")
OUTPUT_STORAGE_PATH = os.path.join(CONFIG.storage_path, "output")

logger = logging.getLogger("ips.storage")


async def store_input_file(file_id: uuid.UUID, input_file: UploadFile) -> None:
    """
    Stores the content of the given uploaded file under the given UUID.
    """
    os.makedirs(INPUT_STORAGE_PATH, exist_ok=True)
    path = os.path.join(INPUT_STORAGE_PATH, str(file_id))

    with open(path, "wb") as fo:
        while True:
            data = await input_file.read(1024)
            if len(data) == 0:
                break

            fo.write(data)
    logger.info("Wrote file content to %s", path)


def get_input_file_path(file_id: uuid.UUID) -> str:
    """
    Returns the path to the input file with the given UUID.
    """
    return os.path.join(INPUT_STORAGE_PATH, str(file_id))


def get_output_file_path(file_id: uuid.UUID) -> str:
    """
    Returns the path to the output file with the given UUID.
    """
    return os.path.join(OUTPUT_STORAGE_PATH, str(file_id))


def create_output_file() -> Tuple[str, str]:
    """
    Creates an output file and returns a pair (UUID, path).
    """
    os.makedirs(OUTPUT_STORAGE_PATH, exist_ok=True)
    file_id = uuid.uuid4()

    return file_id, os.path.join(OUTPUT_STORAGE_PATH, str(file_id))

#!/usr/bin/env python3
import uuid
import os.path
import logging
from fastapi import UploadFile
from .config import CONFIG

INPUT_STORAGE_PATH = os.path.join(CONFIG.storage_path, "input")

logger = logging.getLogger("apiserver.storage")


async def store_input_file(file_id: uuid.UUID, input_file: UploadFile) -> None:
    os.makedirs(INPUT_STORAGE_PATH, exist_ok=True)
    path = os.path.join(INPUT_STORAGE_PATH, str(file_id))

    with open(path, "wb") as fo:
        while True:
            data = await input_file.read(1024)
            if len(data) == 0:
                break

            fo.write(data)
    logger.info("Wrote file content to %s", path)

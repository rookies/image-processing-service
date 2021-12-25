#!/usr/bin/env python3
"""
This file provides access to the file storage that is shared between API server
and workers.
"""
import uuid
import os.path
import logging
from abc import ABC, abstractmethod
from typing import BinaryIO, Optional
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


def get_output_file_path(file_id: uuid.UUID) -> str:
    """
    Returns the path to the output file with the given UUID.
    """
    return os.path.join(OUTPUT_STORAGE_PATH, str(file_id))


class File(ABC):
    """
    Abstract base class for file-related context manager classes. Implements the
    __exit__() method closing the file, the __enter__() method has to be implemented
    by the inheriting class.
    """

    file: Optional[BinaryIO] = None
    path: str = ""

    @abstractmethod
    def __enter__(self):
        ...

    def __exit__(self, *args):
        if self.file is not None:
            self.file.close()
            logger.info("Closed file %s", self.path)
            self.file = None


class InputFile(File):
    """
    Context manager for reading input files, i.e. files uploaded via the API.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, file_id: uuid.UUID):
        self.path = os.path.join(INPUT_STORAGE_PATH, str(file_id))
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "rb")

        logger.info("Opened file %s for reading", self.path)
        return self


class OutputFile(File):
    """
    Context manager for writing output files, i.e. files generated after processing.
    """

    def __init__(self):
        self.uuid = uuid.uuid4()
        self.path = os.path.join(OUTPUT_STORAGE_PATH, str(self.uuid))
        self.file = None

    def __enter__(self):
        os.makedirs(OUTPUT_STORAGE_PATH, exist_ok=True)
        self.file = open(self.path, "wb")

        logger.info("Created file %s and opened it for writing", self.path)
        return self

    def copy_from_file(self, input_file: BinaryIO):
        """
        Copies the content of the given file into the open output file.
        """
        if self.file is None:
            raise RuntimeError(f"File {self.path} is not open")

        while True:
            data = input_file.read(1024)
            if len(data) == 0:
                break

            self.file.write(data)

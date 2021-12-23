#!/usr/bin/env python3
import uuid
import os.path
import logging
from abc import ABC, abstractmethod
from typing import BinaryIO
from .config import CONFIG

INPUT_STORAGE_PATH = os.path.join(CONFIG.storage_path, "input")
OUTPUT_STORAGE_PATH = os.path.join(CONFIG.storage_path, "output")

logger = logging.getLogger("worker.storage")


class File(ABC):
    @abstractmethod
    def __enter__(self):
        ...

    def __exit__(self, *args):
        if self.file is not None:
            self.file.close()
            logger.info("Closed file %s", self.path)
            self.file = None


class InputFile(File):
    def __init__(self, file_id: uuid.UUID):
        self.path = os.path.join(INPUT_STORAGE_PATH, str(file_id))
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "rb")

        logger.info("Opened file %s for reading", self.path)
        return self


class OutputFile(File):
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
        if self.file is None:
            raise RuntimeError("File %s is not open" % self.path)

        while True:
            data = input_file.read(1024)
            if len(data) == 0:
                break

            self.file.write(data)

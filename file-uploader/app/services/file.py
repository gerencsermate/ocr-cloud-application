from datetime import datetime
import os
import shutil
from typing import Annotated, BinaryIO, List

from fastapi import Depends
import httpx

from app.repositories.file_repository import FileRepository
from app.model.db.file import File
from app.utlis.config import get_configuration
from app.utlis.logger import logger
from app.model.api.ocr import OCRRequest, OCRResponse


class FileService:
    def __init__(
        self, file_repository: Annotated[FileRepository, Depends(FileRepository)]
    ):
        self.repository = file_repository
        self.conf = get_configuration()

    async def list_files_for_user(self, user_id: str) -> List[File]:
        files = await self.repository.get_files_by_user(user_id=user_id)
        return files

    async def upload_file(
        self, uploaded_filename: str, file: BinaryIO, uploader_id: str, description: str
    ) -> File:
        _, extension = os.path.splitext(uploaded_filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{uploader_id}_{timestamp}{extension}"
        file_path = os.path.join("UPLOADED_FILES", new_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)

        file = File(
            filename=new_filename, description=description, uploader=uploader_id
        )

        try:
            ocr_data = await self._trigger_ocr_process(new_filename)
            file.ocr_text = ocr_data.found_texts.join(", ")
        except Exception as e:
            logger.error("OCR process failed: %s", str(e))
            raise e

        saved_file = await self.repository.save_file(file=file)

        return saved_file

    async def _trigger_ocr_process(self, filename: str) -> OCRResponse:
        ocr_request = OCRRequest(file_name=filename)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.conf.OCR_URL}/ocr-process",
                json=ocr_request.model_dump_json(),
                timeout=30.0,
            )

            if response.status_code != 200:
                raise ValueError(
                    f"OCR process failed: {response.status_code}, {response.text}"
                )

            ocr_data = OCRResponse(**response.json())
            logger.info("OCR process was successful: %s", ocr_data)
            return ocr_data

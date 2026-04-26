from datetime import datetime
import os
import shutil
from typing import Annotated, BinaryIO, List

from fastapi import Depends

from app.repositories.file_repository import FileRepository
from app.model.db.file import File
from app.utlis.config import get_configuration


class FileService:
    def __init__(
        self, file_repository: Annotated[FileRepository, Depends(FileRepository)]
    ):
        self.repository = file_repository
        self.conf = get_configuration()

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
        saved_file = await self.repository.save_file(file=file)

        return saved_file

    async def list_files_for_user(self, user_id: str) -> List[File]:
        files = await self.repository.get_files_by_user(user_id=user_id)
        return files

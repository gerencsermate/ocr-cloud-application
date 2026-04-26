from typing import List

from bson import ObjectId

from app.model.db.file import File
from app.utlis.logger import logger


class FileRepository:
    async def save_file(self, file: File) -> File:
        saved_file = await file.insert()
        logger.debug("user saved to database, file: %s", self.save_file)
        return saved_file
    
    async def get_all_files(self) -> List[File]:
        files = await File.find_all().to_list()
        logger.debug("Retrieved %d files from database", len(files))
        return files
    
    async def get_files_by_user(self, user_id: str) -> List[File]:
        files = await File.find(File.uploader.id == ObjectId(user_id)).to_list()
        logger.debug("Retrieved %d files for user: %s", len(files), user_id)
        return files
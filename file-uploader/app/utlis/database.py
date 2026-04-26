from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.utlis.config import get_configuration
from app.utlis.logger import logger
from app.model.db.user import User
from app.model.db.file import File


class Database:
    def __init__(self):
        self.client: AsyncMongoClient = None

    async def initialize(self):
        conf = get_configuration()
        self.client = AsyncMongoClient(conf.MONGODB_URL)
        await init_beanie(database=self.client.db_name, document_models=[User, File])
        logger.info(
            "MongoDB connected, db host: %s, db name: %s",
            {self.client.HOST},
            {self.client.db_name},
        )

    def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

from typing import Optional

from beanie import Document, Indexed, Link

from app.model.db.user import User


class File(Document):
    filename: Indexed(str, unique=True)
    description: str
    ocr_text: Optional[list] = None

    uploader: Link[User]

    class Settings:
        name = "files"

from typing import List, Optional

from pydantic import BaseModel, Field

class OCRRequest(BaseModel):
    file_name: str = Field()

class OCRResponse(BaseModel):
    status: str
    file_name: str
    found_texts: Optional[List[str]] = None
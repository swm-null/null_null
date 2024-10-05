from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Memo(BaseModel):
    content: str
    image_urls: list[str]
    metadata: Optional[str]=None
    parent_tag_ids: list[str]=[]
    timestamp: datetime

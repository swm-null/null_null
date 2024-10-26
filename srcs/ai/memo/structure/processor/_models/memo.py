from datetime import datetime
from pydantic import BaseModel


class Memo(BaseModel):
    content: str
    metadata: str=""
    image_urls: list[str]
    parent_tag_ids: list[str]=[]
    timestamp: datetime

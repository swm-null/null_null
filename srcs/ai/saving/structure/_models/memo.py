from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Memo(BaseModel):
    content: str
    metadata: str=""
    parent_tag_ids: list[str]=[]
    timestamp: datetime

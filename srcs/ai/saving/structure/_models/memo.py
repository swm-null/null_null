from datetime import datetime
from pydantic import BaseModel


class Memo(BaseModel):
    content: str
    parent_tag_ids: list[str]=[]
    timestamp: datetime

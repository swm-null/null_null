from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Arg_add_memo(BaseModel):
    content: str
    timestamp: Optional[datetime]

class Res_memo_tag(BaseModel):
    name: str
    id: Optional[str]
    embedding: list[float]
    parent: Optional[str]
    
class Res_add_memo(BaseModel):
    content: str
    memo_embeddings: list[float]
    existing_tag_ids: list[str]
    new_tags: list[Res_memo_tag]
    timestamp: datetime

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Memos_tag(BaseModel):
    name: str
    id: Optional[str]
    embedding: list[float]

class Memos_tag_relation(BaseModel):
    parent_id: Optional[str]
    child_id: str

class Memos_raw_memo(BaseModel):
    content: str
    timestamp: Optional[datetime]=None
    
class Memos_processed_memo(BaseModel):
    timestamp: datetime
    content: str
    parent_tag_ids: list[str]=Field(description="relations between tag and memo")
    tag_relations: list[Memos_tag_relation]=Field(description="relations between tags")
    new_tags: list[Memos_tag]
    embedding: list[float]

class Arg_post_memos(BaseModel):
    content: list[Memos_raw_memo]

class Res_post_memos(BaseModel):
    content: list[Memos_processed_memo]

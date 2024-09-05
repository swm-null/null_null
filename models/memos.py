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
    
class Memos_relations(BaseModel):
    added: list[Memos_tag_relation]
    deleted: list[Memos_tag_relation]

class Memos_raw_memo(BaseModel):
    content: str=Field(examples=["치즈라면 레시피: 라면 위에 치즈를 얹어 내놓는 음식으로 제조법 또한 간단하여 그냥 라면을 끓인 후 시중에 판매되는 슬라이스 체다치즈를 얹는 것으로 완성."])
    timestamp: Optional[datetime]=None
    
class Memos_processed_memo(BaseModel):
    timestamp: datetime
    content: str
    parent_tag_ids: list[str]=Field(description="relations between leaf tags and this memo")
    tag_relations: Memos_relations=Field(description="relations between tags")
    new_tags: list[Memos_tag]
    embedding: list[float]

class Arg_post_memos(BaseModel):
    user_id: str
    memos: list[Memos_raw_memo]

class Res_post_memos(BaseModel):
    processed_memos: list[Memos_processed_memo]

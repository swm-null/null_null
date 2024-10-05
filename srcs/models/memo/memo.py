from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Memo_raw_memo(BaseModel):
    content: str=Field(examples=["치즈라면 레시피: 라면 위에 치즈를 얹어 내놓는 음식으로 제조법 또한 간단하여 그냥 라면을 끓인 후 시중에 판매되는 슬라이스 체다치즈를 얹는 것으로 완성."])
    images: list[str]=[]
    timestamp: Optional[datetime]=None
    
class Memo_processed_memo(BaseModel):
    timestamp: datetime
    content: str
    image_urls: list[str]
    metadata: str
    parent_tag_ids: list[str]=Field(description="relations between leaf tags and this memo")
    embedding: list[float]
    
class Memo_tag_name_and_id(BaseModel):
    id: str
    name: str
    is_new: bool
    
class Memo_tag(BaseModel):
    id: str
    name: str
    is_new: bool
    embedding: Optional[list[float]]=None

class Memo_memo_and_tags(BaseModel):
    content: str=Field(examples=["치즈라면 레시피: 라면 위에 치즈를 얹어 내놓는 음식으로 제조법 또한 간단하여 그냥 라면을 끓인 후 시중에 판매되는 슬라이스 체다치즈를 얹는 것으로 완성."])
    image_urls: list[str]=[]
    timestamp: Optional[datetime]=None
    tags: list[Memo_tag_name_and_id] 
    
class Memo_tag_relation(BaseModel):
    parent_id: str
    child_id: str

class Memo_relations(BaseModel):
    added: list[Memo_tag_relation]
    deleted: list[Memo_tag_relation]

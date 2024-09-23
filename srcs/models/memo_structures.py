from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.memo_tags import Memos_tag

    
class Memos_tag_relation(BaseModel):
    parent_id: str
    child_id: str

class Memos_relations(BaseModel):
    added: list[Memos_tag_relation]
    deleted: list[Memos_tag_relation]
    
class Memos_processed_memo(BaseModel):
    timestamp: datetime
    content: str
    parent_tag_ids: list[str]=Field(description="relations between leaf tags and this memo")
    embedding: list[float]

class Memos_memo_and_tags(BaseModel):
    content: str=Field(examples=["치즈라면 레시피: 라면 위에 치즈를 얹어 내놓는 음식으로 제조법 또한 간단하여 그냥 라면을 끓인 후 시중에 판매되는 슬라이스 체다치즈를 얹는 것으로 완성."])
    timestamp: Optional[datetime]=None
    tags: list[Memos_tag] 
    
class Body_post_memo_structures(BaseModel):
    user_id: str=Field(examples=["add4277c-b56c-4c0c-a14c-8f0a28b5396f"])
    memos: list[Memos_memo_and_tags]
    
class Res_post_memo_structures(BaseModel):
    processed_memos: list[Memos_processed_memo]
    tags_relations: Memos_relations=Field(description="relations between tags")
    new_tags: list[Memos_tag]
    new_structure: dict[str, list[str]]=Field(examples=[{
        "parent_tag_id1": ["child_tag_id1", "child_tag_id2", ],
        "parent_tag_id2": ["child_tag_id2", "child_tag_id3", ],
    }])

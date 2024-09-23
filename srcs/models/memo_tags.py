from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Memos_raw_memo(BaseModel):
    content: str=Field(examples=["치즈라면 레시피: 라면 위에 치즈를 얹어 내놓는 음식으로 제조법 또한 간단하여 그냥 라면을 끓인 후 시중에 판매되는 슬라이스 체다치즈를 얹는 것으로 완성."])
    timestamp: Optional[datetime]=None
    
class Memos_tag(BaseModel):
    name: str
    is_new: bool
    id: str
    embedding: Optional[list[float]]=None
    
class Body_post_memo_tags(BaseModel):
    user_id: str=Field(examples=["add4277c-b56c-4c0c-a14c-8f0a28b5396f"])
    raw_memos: list[Memos_raw_memo]
    
class Res_post_memo_tags(BaseModel):
    tags: list[list[Memos_tag]]

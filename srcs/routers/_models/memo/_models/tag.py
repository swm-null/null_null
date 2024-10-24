from typing import Optional
from pydantic import BaseModel

    
class Memo_tag(BaseModel):
    id: str
    name: str
    is_new: bool
    embedding: Optional[list[float]]=None

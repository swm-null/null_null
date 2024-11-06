from pydantic import BaseModel

    
class Memo_tag(BaseModel):
    id: str
    name: str
    is_new: bool
    embedding: list[float]=[]

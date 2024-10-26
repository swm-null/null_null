from pydantic import BaseModel

    
class Memo_tag_name_and_id(BaseModel):
    id: str
    name: str
    is_new: bool

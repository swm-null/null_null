from pydantic import BaseModel
from models.memo_tags import Memos_tag, Memos_raw_memo


class Body_post_memo_tag(BaseModel):
    user_id: str
    raw_memo: Memos_raw_memo
    
class Res_post_memo_tag(BaseModel):
    tags: list[Memos_tag]

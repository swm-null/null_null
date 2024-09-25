from pydantic import BaseModel, Field
from models.memo import Memo_raw_memo, Memo_tag_name_and_id


class Body_post_memo_tags(BaseModel):
    user_id: str=Field(examples=["add4277c-b56c-4c0c-a14c-8f0a28b5396f"])
    raw_memos: list[Memo_raw_memo]
    
class Res_post_memo_tags(BaseModel):
    tags: list[list[Memo_tag_name_and_id]]

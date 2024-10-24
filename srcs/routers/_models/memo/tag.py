from pydantic import BaseModel
from routers._models.memo import Memo_raw_memo, Memo_tag_name_and_id


class Body_post_memo_tag(BaseModel):
    user_id: str
    raw_memo: Memo_raw_memo
    
class Res_post_memo_tag(BaseModel):
    tags: list[Memo_tag_name_and_id]

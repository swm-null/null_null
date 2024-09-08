from pydantic import BaseModel
from models.memos import Memos_raw_memo, Memos_processed_memo


class Arg_post_memo(BaseModel):
    user_id: str
    memo: Memos_raw_memo

class Res_post_memo(BaseModel):
    processed_memo: Memos_processed_memo
    new_structure: dict[str, list[str]]

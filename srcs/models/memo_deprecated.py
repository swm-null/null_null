from pydantic import BaseModel
from models.memos_deprecated import Memo_raw_memo, Memo_processed_memo


class Arg_post_memo(BaseModel):
    user_id: str
    memo: Memo_raw_memo

class Res_post_memo(BaseModel):
    processed_memo: Memo_processed_memo
    new_structure: dict[str, list[str]]

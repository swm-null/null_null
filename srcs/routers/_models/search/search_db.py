from pydantic import BaseModel


class Arg_post_search_db(BaseModel):
    user_id: str
    content: str

class Res_post_search_db(BaseModel):
    memo_ids: list[str]

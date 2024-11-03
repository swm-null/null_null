from pydantic import BaseModel


class Arg_post_search_db(BaseModel):
    user_id: str
    query: str

class Res_post_search_db(BaseModel):
    memo_ids: list[str]

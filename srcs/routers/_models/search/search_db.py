from re import Pattern
from typing import Optional
from pydantic import BaseModel, Field
from routers._models.search import Search_query_type


class Arg_post_search_db(BaseModel):
    user_id: str
    content: str

class Res_post_search_db(BaseModel):
    memos: list[str]

from re import Pattern
from typing import Optional
from pydantic import BaseModel, Field
from routers._models.search import Search_query_type


class Arg_post_search_ai(BaseModel):
    user_id: str
    query: str

class Res_post_search_ai(BaseModel):
    type: Search_query_type
    # similarity
    processed_message: Optional[str]=Field(default=None)
    memo_ids: Optional[list[str]]=Field(description="used memo ids for processing message", default=None)
    # regex
    regex: Optional[Pattern[str]]=Field(default=None)

from re import Pattern
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Search_query_type(Enum):
    regex = "regex"
    similarity = "similarity"

class Arg_post_search(BaseModel):
    user_id: str
    content: str

class Res_post_search(BaseModel):
    type: Search_query_type
    # similarity
    processed_message: Optional[str]=Field(default=None)
    ids: Optional[list[str]]=Field(description="used memo ids for processing message", default=None)
    # regex
    regex: Optional[Pattern[str]]=Field(default=None)

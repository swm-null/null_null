from re import Pattern
from typing import Optional
from pydantic import BaseModel, Field
from ai.searching._models.query_type import Query_Type

class Arg_post_search(BaseModel):
    user_id: str
    content: str

class Res_post_search(BaseModel):
    type: Query_Type
    # similarity
    processed_message: Optional[str]=Field(default=None)
    ids: Optional[list[str]]=Field(description="used memo ids for processing message", default=None)
    # regex
    regex: Optional[Pattern[str]]=Field(default=None)

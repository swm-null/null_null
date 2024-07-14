from pydantic import BaseModel
from typing import Optional
from ai.for_search import query_analyzer as qa

class Arg_search(BaseModel):
    query: str

class Res_search(BaseModel):
    type: qa.Query_Type=qa.Query_Type.unspecified
    processed_message: Optional[str]=None
    ids: Optional[list[str]]=None
    regex: Optional[str]=None
    tags: Optional[list[str]]=None

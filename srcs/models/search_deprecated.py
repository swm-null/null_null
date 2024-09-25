from pydantic import BaseModel
from typing import Optional
from ai.searching_deprecated import query_analyzer as qa

class Arg_search(BaseModel):
    content: str

class Res_search(BaseModel):
    type: qa.Search_Query_Type=qa.Search_Query_Type.unspecified
    processed_message: Optional[str]=None
    ids: Optional[list[str]]=None
    regex: Optional[str]=None
    tags: Optional[list[str]]=None

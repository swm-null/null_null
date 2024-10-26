from typing import Optional
from pydantic import BaseModel


class Tag(BaseModel):
    id: str
    name: str
    is_new: bool
    connected_memo_id: Optional[int]=None

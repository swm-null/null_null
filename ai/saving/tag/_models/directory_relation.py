from typing import Optional
from pydantic import BaseModel


class Directory_relation(BaseModel):
    parent_id: Optional[str]
    parent_name: Optional[str]
    child_id: str
    child_name: str
    is_new: bool
    
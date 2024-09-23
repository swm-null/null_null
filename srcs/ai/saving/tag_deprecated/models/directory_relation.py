from pydantic import BaseModel


class Directory_relation(BaseModel):
    parent_id: str
    parent_name: str
    child_id: str
    child_name: str
    is_new: bool
    
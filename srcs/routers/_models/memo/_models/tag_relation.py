from pydantic import BaseModel


class Memo_tag_relation(BaseModel):
    parent_id: str
    child_id: str

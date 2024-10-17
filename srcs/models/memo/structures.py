from pydantic import BaseModel, Field
from models.memo import Memo_tag, Memo_relations, Memo_processed_memo, Memo_memo_and_tags

    
class Body_post_memo_structures(BaseModel):
    user_id: str=Field(examples=["add4277c-b56c-4c0c-a14c-8f0a28b5396f"])
    memos: list[Memo_memo_and_tags]
    
class Res_post_memo_structures(BaseModel):
    processed_memos: list[Memo_processed_memo]
    new_tags: list[Memo_tag]
    new_structure: dict[str, list[str]]=Field(examples=[{
        "parent_tag_id1": ["child_tag_id1", "child_tag_id2", ],
        "parent_tag_id2": ["child_tag_id2", "child_tag_id3", ],
    }])
    new_reversed_structure: dict[str, list[str]]=Field(examples=[{
        "child_tag_id1": ["parent_tag_id1", "parent_tag_id2", ],
        "child_tag_id2": ["parent_tag_id2", "parent_tag_id3", ],
    }])

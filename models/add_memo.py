from pydantic import BaseModel

class Arg_add_memo(BaseModel):
    content: str

class Res_memo(BaseModel):
    name: str
    embedding: list[float]
    
class Res_add_memo(BaseModel):
    memo_embeddings: list[float]
    existing_tag_ids: list[str]
    new_tags: list[Res_memo]

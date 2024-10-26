from datetime import datetime
from pydantic import BaseModel, Field

    
class Memo_processed_memo(BaseModel):
    timestamp: datetime
    content: str
    image_urls: list[str]
    metadata: str
    parent_tag_ids: list[str]=Field(description="relations between leaf tags and this memo")
    embedding: list[float]
    embedding_metadata: list[float]=[]

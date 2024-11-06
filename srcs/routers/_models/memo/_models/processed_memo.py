from datetime import datetime
from pydantic import BaseModel, Field
from routers._models.memo._models import Memo_tag_name_and_id

    
class Memo_processed_memo(BaseModel):
    timestamp: datetime
    content: str
    image_urls: list[str]
    voice_urls: list[str]
    metadata: str
    temporal_tags: list[Memo_tag_name_and_id] | None
    parent_tag_ids: list[str]=Field(description="relations between leaf tags and this memo")
    embedding: list[float]
    embedding_metadata: list[float]

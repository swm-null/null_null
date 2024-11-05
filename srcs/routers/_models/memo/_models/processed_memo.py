from datetime import datetime
from pydantic import BaseModel, Field

    
class Memo_processed_memo(BaseModel):
    timestamp: datetime | None
    content: str | None
    image_urls: list[str] | None
    voice_urls: list[str] | None
    metadata: str | None
    parent_tag_ids: list[str] | None=Field(description="relations between leaf tags and this memo")
    embedding: list[float] | None
    embedding_metadata: list[float] | None

from datetime import datetime
from pydantic import BaseModel


class Memo(BaseModel):
    id: str
    content: str
    timestamp: datetime

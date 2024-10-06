from datetime import datetime
from pydantic import BaseModel


class Memo(BaseModel):
    id: str
    metadata: str
    content: str
    timestamp: datetime
    
    def __hash__(self):
        return hash(id)

    def __eq__(self, other):
        if isinstance(other, Memo):
            return self.id==other.id
        return False

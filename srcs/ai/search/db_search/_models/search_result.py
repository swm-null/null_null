from pydantic import BaseModel


class Search_result(BaseModel):
    memo_id: str
    score: float

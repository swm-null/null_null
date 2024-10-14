from typing import Optional
from pydantic import BaseModel, Field


class Similarity_search_agent_output(BaseModel):
    action: Optional[str]=None
    action_input: Optional[dict[str, str]]=None
    final_answer: Optional[str]=Field(description="answer to the user's question")
    used_memo_ids: list[str]=Field(description="used memo ids", default=[])

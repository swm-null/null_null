from datetime import datetime
from langchain_core.tools import tool
from openai import BaseModel
from pydantic import Field
from ai.search._models.memo import Memo
from ai.search.ai_search.utils.similarity.utils.retrieve_similar_memos_from_db import retrieve_similar_memos_from_db, aretrieve_similar_memos_from_db
from ai.search.ai_search.utils.similarity.utils.chains.similarity_result_with_memo_chain import asimilarity_result_with_memo, similarity_result_with_memo, Similarity_result_with_memo_chain_output
from fastapi.concurrency import run_in_threadpool


class _memo_answer_args(BaseModel):
    user_id: str=Field(description="user's id")
    question: str=Field(description="user's question")
    language: str=Field(description="user's language")

@tool("memo_answerer", args_schema=_memo_answer_args, return_direct=False)
def memo_answerer(user_id: str, question: str, keyword: str, start_time: datetime, end_time: datetime, language: str) -> Similarity_result_with_memo_chain_output:
    """Use the user's memos to check if the given question can be answered, and if so, obtain the answer."""
    retrieved_memos: list[Memo]=retrieve_similar_memos_from_db(question, keyword, user_id, start_time, end_time)
    
    return similarity_result_with_memo(question, retrieved_memos, language)

async def amemo_answerer(user_id: str, question: str, keyword: str, start_time: datetime, end_time: datetime, language: str) -> Similarity_result_with_memo_chain_output:
    """Use the user's memos to check if the given question can be answered, and if so, obtain the answer."""
    retrieved_memos: list[Memo]=await aretrieve_similar_memos_from_db(question, keyword, user_id, start_time, end_time)
    
    return await asimilarity_result_with_memo(question, retrieved_memos, language)

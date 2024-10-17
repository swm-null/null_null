from typing import Any, Coroutine
from langchain_core.tools import tool
from openai import BaseModel
from pydantic import Field
from ai.searching._models.memo import Memo
from ai.searching.utils.retrieve_similar_memos_from_db import retrieve_similar_memos_from_db
from ai.searching.utils.format_memos import format_memos
from ai.searching.utils.chains.similarity_result_with_memo_chain import similarity_result_with_memo_chain, Similarity_result_with_memo_chain_output
from fastapi.concurrency import run_in_threadpool


class _memo_answer_args(BaseModel):
    user_id: str=Field(description="user's id")
    question: str=Field(description="user's question")
    language: str=Field(description="user's language")

@tool("memo_answerer", args_schema=_memo_answer_args, return_direct=False)
def memo_answerer(user_id: str, question: str, language: str) -> Similarity_result_with_memo_chain_output:
    """Use the user's memos to check if the given question can be answered, and if so, obtain the answer."""
    retrieved_memos: list[Memo]=retrieve_similar_memos_from_db(question, user_id)
    formatted_memos: str=format_memos(retrieved_memos)
    
    return similarity_result_with_memo_chain.invoke({
            "question": question,
            "memo_context": formatted_memos,
            "language": language,
    })
    
async def amemo_answerer(user_id: str, question: str, language: str) -> Similarity_result_with_memo_chain_output:
    """Use the user's memos to check if the given question can be answered, and if so, obtain the answer."""
    retrieved_memos: list[Memo]=await run_in_threadpool(retrieve_similar_memos_from_db, question, user_id)
    formatted_memos: str=format_memos(retrieved_memos)
    
    return await similarity_result_with_memo_chain.ainvoke({
            "question": question,
            "memo_context": formatted_memos,
            "language": language,
    })

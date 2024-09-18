import logging
from ai.searching.models.memo import Memo
from ai.searching.utils.chains.generate_similarity_result_chain import generate_similarity_result_chain

def generate_similarity_result(query: str, memos: list[Memo], lang: str="Korean") -> tuple[str, list[str]]:
    formatted_memos: str=_format_memos(memos)
    generated_result=generate_similarity_result_chain.invoke({"query": query, "context": formatted_memos, "lang": lang})
    logging.info("[generate similarity result]\n## %s\n%s\n\n", generated_result.answer, generated_result.used_memo_ids)
    
    return generated_result.answer, generated_result.used_memo_ids
    
def _format_memos(memos: list[Memo]) -> str:
    formatted_memos: str=""
    
    for memo in memos:
        formatted_memos+=f"ID: {memo.id}, {memo.timestamp}\n"
        formatted_memos+=f"{memo.content}\n\n"
        
    return formatted_memos

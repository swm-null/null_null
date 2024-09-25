import logging
from fastapi import HTTPException
from ai.searching._models import Memo
from ai.searching.utils.chains import generate_similarity_result_chain


def generate_similarity_result(query: str, memos: list[Memo], lang: str="Korean") -> tuple[str, list[str]]:
    formatted_memos: str=_format_memos(memos)
    generated_result=generate_similarity_result_chain.invoke({"query": query, "context": formatted_memos, "lang": lang})
    logging.info("[generate similarity result]\n## %s\n%s\n\n", generated_result.answer, generated_result.used_memo_ids)
    _validate_result(memos, generated_result.used_memo_ids)
    
    return generated_result.answer, generated_result.used_memo_ids
    
def _format_memos(memos: list[Memo]) -> str:
    return "\n".join(f"""
            ID: {memo.id}, {memo.timestamp}\n
            {memo.content}\n
        """ for memo in memos
    )

def _validate_result(memos: list[Memo], used_memo_ids: list[str]) -> None:
    missing_ids = [used_memo_id for used_memo_id in used_memo_ids if not any(memo.id == used_memo_id for memo in memos)]
    if missing_ids:
        logging.error("[_validate_result]\n## %s\n\n", missing_ids)
        raise HTTPException(status_code=500, headers={"/search._validate_result": str(missing_ids)})

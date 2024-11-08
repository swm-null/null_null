import asyncio
from datetime import datetime
import logging
from ai.search.ai_search.utils.similarity.utils import invoke_similarity_search_agent, amemo_answerer
from ai.search.ai_search.utils.similarity.utils.chains.similarity_result_with_memo_chain import Similarity_result_with_memo_chain_output


async def generate_similarity_result(user_id: str, query: str, keyword: str, start_time: datetime, end_time: datetime, lang: str="Korean") -> tuple[str, list[str]]:
    generated_answer, used_memo_ids=await _generate_similarity_result(user_id, query, keyword, start_time, end_time, lang)
    logging.info("[/Search.generate_similarity_result]\n## %s\n%s\n\n", generated_answer, used_memo_ids)
    
    return generated_answer, used_memo_ids

async def _generate_similarity_result(user_id: str, query: str, keyword: str, start_time: datetime, end_time: datetime, lang: str) -> tuple[str, list[str]]:
    task_using_memo=await asyncio.create_task(amemo_answerer(user_id, query, keyword, start_time, end_time, lang))
    
    return task_using_memo.answer, task_using_memo.used_memo_ids

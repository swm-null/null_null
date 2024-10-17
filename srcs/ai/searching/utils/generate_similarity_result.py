import asyncio
import logging
from ai.searching.utils.agents.similarity_search_agent import invoke_similarity_search_agent
from ai.searching.utils.agents.tools import amemo_answerer
from ai.searching.utils.chains.similarity_result_with_memo_chain import Similarity_result_with_memo_chain_output


async def generate_similarity_result(user_id: str, query: str, lang: str="Korean") -> tuple[str, list[str]]:
    generated_answer, used_memo_ids=await _generate_similarity_result(user_id, query, lang)
    logging.info("[/Search.generate_similarity_result]\n## %s\n%s\n\n", generated_answer, used_memo_ids)
    
    return generated_answer, used_memo_ids

async def _generate_similarity_result(user_id: str, query: str, lang: str) -> tuple[str, list[str]]:
    task_using_memo=asyncio.create_task(amemo_answerer(user_id, query, lang))
    task_using_internet=asyncio.create_task(invoke_similarity_search_agent(user_id, query, lang))
    
    done, pending = await asyncio.wait(
        [task_using_memo, task_using_internet], # type: ignore
        return_when=asyncio.FIRST_COMPLETED
    )
    
    task_using_memo_result: Similarity_result_with_memo_chain_output=await task_using_memo
    if task_using_memo_result.answerable:
        task_using_internet.cancel()
        try:
            await task_using_internet
        except asyncio.CancelledError:
            pass
        return task_using_memo_result.answer, task_using_memo_result.used_memo_ids
    else:
        return await task_using_internet

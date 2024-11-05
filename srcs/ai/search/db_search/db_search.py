import asyncio
from fastapi.concurrency import run_in_threadpool
from ai.search.db_search._models import Search_result
from ai.utils import embedder
from routers._models.search import Res_post_search_db
from ai.search.db_search.utils import perform_keyword_query_by_keyword, perform_query_by_vector
from ai.search.utils import keyword_query_generator, convert_timezone


async def search_memo_using_db(query: str, user_id: str, lang: str="Korean") -> Res_post_search_db:
    generated_query, embedding=await asyncio.gather(
        keyword_query_generator(query, lang),
        embedder.aembed_query(query)
    )
    start_time, end_time=convert_timezone(generated_query.start_time, generated_query.end_time, lang)

    keyword_results, vector_results=await asyncio.gather(
        run_in_threadpool(perform_keyword_query_by_keyword, generated_query.query, start_time, end_time, user_id),
        perform_query_by_vector(embedding, start_time, end_time, user_id),
    )
    combined_results=_combine_results(keyword_results, vector_results)
    
    return Res_post_search_db(
        memo_ids=[result.memo_id for result in combined_results]
    )

def _combine_results(keyword_results: list[Search_result], vector_results: list[Search_result]) -> list[Search_result]:
    keyword_id_to_score: dict[str, float]={result.memo_id: result.score for result in keyword_results}
    vector_id_to_score: dict[str, float]={result.memo_id: result.score for result in vector_results}

    combined_result: list[Search_result]=[]
    for key in keyword_id_to_score.keys():
        combined_result.append(Search_result(
            memo_id=key,
            score=keyword_id_to_score.get(key, 0)*1+vector_id_to_score.get(key, 0)*3
        ))
        
    return sorted(combined_result, key=lambda result: result.score, reverse=True)

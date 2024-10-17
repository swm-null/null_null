from re import Pattern
from models.search import Res_post_search
from ai.searching.utils import generate_similarity_result, query_analyzer, generate_regex
from models.search import Search_query_type


async def search_memo(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    query_Type: Search_query_type=await query_analyzer(query, lang)
    
    if query_Type==Search_query_type.regex:
        return await _regex(query, lang)
    else:
        return await _similarity(query, user_id, lang)
    
async def _regex(query: str, lang: str="Korean") -> Res_post_search:
    generated_regex: Pattern[str]=await generate_regex(query, lang)
    
    return Res_post_search(
        type=Search_query_type.regex,
        regex=generated_regex
    )
    
async def _similarity(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    generated_answer, used_memo_ids=await generate_similarity_result(user_id, query, lang)
    
    return Res_post_search(
        type=Search_query_type.similarity,
        processed_message=generated_answer,
        ids=used_memo_ids
    )
    
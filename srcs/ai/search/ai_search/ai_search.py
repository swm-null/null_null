import asyncio
from routers._models import Res_post_search_ai, Search_query_type
from ai.search.ai_search.utils import regex, similarity, query_analyzer
from ai.search.utils import keyword_query_generator, convert_timezone


async def search_memo_using_ai(query: str, user_id: str, lang: str="Korean") -> Res_post_search_ai:
    query_Type, generated_query=await asyncio.gather(
        query_analyzer(query, lang),
        keyword_query_generator(query, lang)
    )
    start_time, end_time=convert_timezone(generated_query.start_time, generated_query.end_time, lang)
    
    if query_Type==Search_query_type.regex:
        return await regex(query, lang)
    else:
        return await similarity(query, user_id, generated_query.query, start_time, end_time, lang)

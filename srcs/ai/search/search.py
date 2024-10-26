from routers._models import Res_post_search, Search_query_type
from ai.search.utils import regex, similarity, query_analyzer


async def search_memo(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    query_Type: Search_query_type=await query_analyzer(query, lang)
    
    if query_Type==Search_query_type.regex:
        return await regex(query, lang)
    else:
        return await similarity(query, user_id, lang)

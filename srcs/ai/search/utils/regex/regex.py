from re import Pattern
from routers._models import Res_post_search_ai, Search_query_type
from ai.search.utils.regex.utils import generate_regex


async def regex(query: str, lang: str="Korean") -> Res_post_search_ai:
    generated_regex: Pattern[str]=await generate_regex(query, lang)
    
    return Res_post_search_ai(
        type=Search_query_type.regex,
        regex=generated_regex
    )

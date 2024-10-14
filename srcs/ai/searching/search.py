from re import Pattern
from models.search import Res_post_search
from ai.searching.utils import generate_similarity_result, query_analyzer, generate_regex
from ai.searching._models import Memo
from models.search import Search_query_type


def search_memo(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    query_Type: Search_query_type=query_analyzer(query, lang)
    
    if query_Type==Search_query_type.regex:
        return _regex(query, lang)
    else:
        return _similarity(query, user_id, lang)
    
def _regex(query: str, lang: str="Korean") -> Res_post_search:
    generated_regex: Pattern[str]=generate_regex(query, lang)
    
    return Res_post_search(
        type=Search_query_type.regex,
        regex=generated_regex
    )
    
def _similarity(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    generated_answer, used_memo_ids=generate_similarity_result(user_id, query, lang)
    
    return Res_post_search(
        type=Search_query_type.similarity,
        processed_message=generated_answer,
        ids=used_memo_ids
    )
    
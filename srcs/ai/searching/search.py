from re import Pattern
from models.search import Res_post_search
from ai.searching.utils.generate_similarity_result import generate_similarity_result
from ai.searching.utils.retrieve_similar_memos_from_db import retrieve_similar_memos_from_db
from ai.searching.utils.query_analyzer import analyzer
from ai.searching.models.query_type import Query_Type
from ai.searching.models.memo import Memo
from ai.searching.utils.generate_regex import generate_regex


def search(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    query_type: Query_Type=analyzer(query, lang)
    
    if query_type==Query_Type.regex:
        return _regex(query, lang)
    else:
        return _similarity(query, user_id, lang)
    
def _regex(query: str, lang: str="Korean") -> Res_post_search:
    generated_regex: Pattern[str]=generate_regex(query, lang)
    
    return Res_post_search(
        type=Query_Type.regex,
        regex=generated_regex
    )
    
def _similarity(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    similar_memos: list[Memo]=retrieve_similar_memos_from_db(query, user_id)
    generated_answer: str
    used_memo_ids: list[str]
    generated_answer, used_memo_ids=generate_similarity_result(query, similar_memos, lang)
    
    return Res_post_search(
        type=Query_Type.similarity,
        processed_message=generated_answer,
        ids=used_memo_ids
    )
    
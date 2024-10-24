from ai.search.utils.similarity.utils import generate_similarity_result
from routers._models import Res_post_search, Search_query_type


async def similarity(query: str, user_id: str, lang: str="Korean") -> Res_post_search:
    generated_answer, used_memo_ids=await generate_similarity_result(user_id, query, lang)
    
    return Res_post_search(
        type=Search_query_type.similarity,
        processed_message=generated_answer,
        ids=used_memo_ids
    )
    
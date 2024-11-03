from ai.search.ai_search.utils.similarity.utils import generate_similarity_result
from routers._models import Res_post_search_ai, Search_query_type


async def similarity(query: str, user_id: str, lang: str="Korean") -> Res_post_search_ai:
    generated_answer, used_memo_ids=await generate_similarity_result(user_id, query, lang)
    
    return Res_post_search_ai(
        type=Search_query_type.similarity,
        processed_message=generated_answer,
        memo_ids=used_memo_ids
    )

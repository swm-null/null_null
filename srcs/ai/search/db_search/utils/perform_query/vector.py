import asyncio
from datetime import datetime
from ai.search.db_search._models.search_result import Search_result
from ai.utils.database.collections.memo_store import *
from fastapi.concurrency import run_in_threadpool


async def perform_query_by_vector(embedding: list[float], start_time: datetime, end_time: datetime, user_id: str) -> list[Search_result]:
    metadata_search_result, content_search_result=await asyncio.gather(
        run_in_threadpool(_search_metadata_by_vector, embedding, start_time, end_time, user_id),
        run_in_threadpool(_search_content_by_vector, embedding, start_time, end_time, user_id),
    )

    metadata_id_to_score: dict[str, float]={result[MEMO_ID_NAME]: result["score"] for result in metadata_search_result}
    content_id_to_score: dict[str, float]={result[MEMO_ID_NAME]: result["score"] for result in content_search_result}
    
    combined_keys = set(metadata_id_to_score.keys()).union(set(content_id_to_score.keys()))
    combined_result: list[Search_result]=[]
    for key in combined_keys:
        combined_result.append(Search_result(
            memo_id=key,
            score=metadata_id_to_score.get(key, 0)+content_id_to_score.get(key, 0) # 0 to 2
        ))
    
    return combined_result

def _search_metadata_by_vector(embedding: list[float], start_time: datetime, end_time: datetime, user_id: str):
    return memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_METADATA_INDEX_NAME,
                'path': MEMO_METADATA_EMBEDDING_PATH,
                'queryVector': embedding,
                'numCandidates': 1000,
                'limit': 15,
                'filter': { 
                    MEMO_UID_NAME: user_id
                }
            }
        },
        {
            "$project": 
            {
                MEMO_ID_NAME: 1,
                "score": { "$meta": "vectorSearchScore" } # [0, 1]
            }
        }
    ])

def _search_content_by_vector(embedding: list[float], start_time: datetime, end_time: datetime, user_id: str):
    return memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_INDEX_NAME,
                'path': MEMO_CONTENT_EMBEDDING_PATH,
                'queryVector': embedding,
                'numCandidates': 1000,
                'limit': 15,
                'filter': { 
                    MEMO_UID_NAME: user_id
                }
            }
        },
        {
            "$project": 
            {
                MEMO_ID_NAME: 1,
                "score": { "$meta": "vectorSearchScore" } # [0, 1]
            }
        }
    ])

import logging
from ai.searching._models import Memo
from ai.database.collections.memo_store import MEMO_CONTENT_NAME, MEMO_ID_NAME, MEMO_UID_NAME, MEMO_UTIME_NAME, memo_collection, MEMO_INDEX_NAME
from ai.utils import embedder

def retrieve_similar_memos_from_db(query: str, user_id: str) -> list[Memo]:
    raw_memos=_get_memos_from_db(query, user_id)
    memos: list[Memo]=_memos_from_raw_memos(raw_memos)
    logging.info("[retrieved memos]\n## %s\n%s\n\n", user_id, memos)
    
    return memos
    
    
def _get_memos_from_db(query: str, user_id: str):        
    return memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_INDEX_NAME,
                'path': "embedding",
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 20,
            }
        },
        {
            "$project": 
            {
                MEMO_ID_NAME: 1,
                MEMO_CONTENT_NAME: 1,
                MEMO_UTIME_NAME: 1,
            }
        },
        {
            "$match":
            {
                "$expr": { MEMO_UID_NAME: user_id}
            }
        }
    ])

def _memos_from_raw_memos(raw_memos) -> list[Memo]:
    memos: list[Memo]=[]
    
    for memo in raw_memos:
        memos.append(Memo(
            id=memo[MEMO_ID_NAME],
            content=memo[MEMO_CONTENT_NAME],
            timestamp=memo[MEMO_UTIME_NAME],
        ))
        
    return memos

import logging
from ai.searching._models import Memo
from ai.database.collections.memo_store import *
from ai.utils import embedder

def retrieve_similar_memos_from_db(query: str, user_id: str) -> list[Memo]:
    memos: set[Memo]=_get_memos_from_db_using_content(query, user_id) | _get_memos_from_db_using_metadata(query, user_id)
    logging.info("[retrieved memos]\n## %s\n%s\n\n", user_id, memos)
    
    return list(memos)
    
    
# TODO: async query vector
def _get_memos_from_db_using_content(query: str, user_id: str) -> set[Memo]:
    raw_memos=memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_INDEX_NAME,
                'path': MEMO_CONTENT_EMBEDDING_PATH,
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 15,
                'filter': { MEMO_UID_NAME: user_id }
            }
        },
        {
            "$project": 
            {
                MEMO_ID_NAME: 1,
                MEMO_CONTENT_NAME: 1,
                MEMO_UTIME_NAME: 1,
                MEMO_METADATA_NAME: 1,
            }
        }
    ])
    
    return {
        Memo(
            id=memo[MEMO_ID_NAME],
            metadata=memo[MEMO_METADATA_NAME],
            content=memo[MEMO_CONTENT_NAME],
            timestamp=memo[MEMO_UTIME_NAME],
        ) for memo in raw_memos
    }
        
def _get_memos_from_db_using_metadata(query: str, user_id: str) -> set[Memo]:
    raw_memos=memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_METADATA_INDEX_NAME,
                'path': MEMO_METADATA_EMBEDDING_PATH,
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 15,
                'filter': { MEMO_UID_NAME: user_id }
            }
        },
        {
            "$project": 
            {
                MEMO_ID_NAME: 1,
                MEMO_CONTENT_NAME: 1,
                MEMO_UTIME_NAME: 1,
                MEMO_METADATA_NAME: 1,
            }
        }
    ])
    
    return {
        Memo(
            id=memo[MEMO_ID_NAME],
            metadata=memo[MEMO_METADATA_NAME],
            content=memo[MEMO_CONTENT_NAME],
            timestamp=memo[MEMO_UTIME_NAME],
        ) for memo in raw_memos
    }

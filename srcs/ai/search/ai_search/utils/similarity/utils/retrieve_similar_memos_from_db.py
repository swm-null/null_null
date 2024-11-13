import asyncio
from datetime import datetime
import logging
from ai.search._models import Memo
from ai.utils.database import *
from ai.utils import embedder
from fastapi.concurrency import run_in_threadpool

def retrieve_similar_memos_from_db(query: str, keyword: str, user_id: str, start_time: datetime, end_time: datetime,) -> list[Memo]:
    memos: set[Memo]=_get_memos_from_db_using_content(query, user_id, start_time, end_time) \
                    | _get_memos_from_db_using_metadata(query, user_id, start_time, end_time) \
                    | _perform_keyword_query(keyword, start_time, end_time, user_id)
    logging.info("[retrieved memos]\n## %s\n%s\n\n", user_id, memos)
    
    return list(memos)
    
async def aretrieve_similar_memos_from_db(query: str, keyword: str, user_id: str, start_time: datetime, end_time: datetime,) -> list[Memo]:
    memos: set[Memo]=set().union(*(await asyncio.gather(
        run_in_threadpool(_get_memos_from_db_using_content, query, user_id, start_time, end_time),
        run_in_threadpool(_get_memos_from_db_using_metadata, query, user_id, start_time, end_time),
        run_in_threadpool(_perform_keyword_query, keyword, start_time, end_time, user_id)
    )))
    logging.info("[retrieved memos]\n## %s\n%s\n\n", user_id, memos)
    
    return list(memos)
    
def _get_memos_from_db_using_content(query: str, user_id: str, start_time: datetime, end_time: datetime) -> set[Memo]:
    raw_memos=memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_INDEX_NAME,
                'path': MEMO_CONTENT_EMBEDDING_PATH,
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 10,
                'filter': {
                    "$and": [
                        { MEMO_UID_NAME: user_id },
                        {
                            MEMO_UTIME_NAME: {
                                "$gte": start_time,
                                "$lte": end_time
                            }
                        }
                    ]
                }
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
        
def _get_memos_from_db_using_metadata(query: str, user_id: str, start_time: datetime, end_time: datetime) -> set[Memo]:
    raw_memos=memo_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': MEMO_METADATA_INDEX_NAME,
                'path': MEMO_METADATA_EMBEDDING_PATH,
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 10,
                'filter': {
                    "$and": [
                        { MEMO_UID_NAME: user_id },
                        {
                            MEMO_UTIME_NAME: {
                                "$gte": start_time,
                                "$lte": end_time
                            }
                        }
                    ]
                }
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

def _perform_keyword_query(query: str, start_time: datetime, end_time: datetime, user_id: str) -> set[Memo]: 
    raw_memos=memo_collection.aggregate([
        {
            "$search": {
                "index": MEMO_SEARCH_INDEX_NAME,
                "compound": {
                    "should": [
                        {
                            "autocomplete": {
                                "query": query, 
                                "path": MEMO_CONTENT_NAME
                            }
                        }, 
                        {
                            "autocomplete": {
                                "query": query,
                                "path": MEMO_METADATA_NAME
                            }
                        }
                    ], 
                    "minimumShouldMatch": 1
                }
            }
        }, 
        {
            "$match": {
                MEMO_UID_NAME: user_id,
                MEMO_UTIME_NAME: {
                    "$gte": start_time,
                    "$lte": end_time
                }
            }
        },
        {
            "$addFields": {
                "score": {
                "$meta": "searchScore"
                }
            }
        },
        { "$limit": 10 },
        {
            "$project": {
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

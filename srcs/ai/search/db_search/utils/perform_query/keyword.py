from datetime import datetime
from ai.search.db_search._models.search_result import Search_result
from ai.utils.database.collections.memo_store import *


def perform_keyword_query_by_keyword(query: str, start_time: datetime, end_time: datetime, user_id: str) -> list[Search_result]: 
    search_result=memo_collection.aggregate([
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
                "score": 1 # [0, inf?]
            }
        }
    ])
    
    return [
        Search_result(
            memo_id=memo[MEMO_ID_NAME],
            score=memo["score"]
        ) for memo in search_result
    ]

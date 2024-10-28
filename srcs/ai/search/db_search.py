from ai.utils.database.collections import memo_collection, MEMO_UID_NAME, MEMO_CONTENT_NAME, MEMO_METADATA_NAME, MEMO_SEARCH_INDEX_NAME, MEMO_ID_NAME
from routers._models.search import Res_post_search_db


def search_memo_using_db(query: str, user_id: str) -> Res_post_search_db:
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
                MEMO_UID_NAME: user_id
            }
        },
        {
            "$limit": 3
        }, 
        {
            "$project": {
                MEMO_ID_NAME: 1,
            }
        }
    ])
    
    return Res_post_search_db(
        memos=[memo[MEMO_ID_NAME] for memo in search_result]
    )

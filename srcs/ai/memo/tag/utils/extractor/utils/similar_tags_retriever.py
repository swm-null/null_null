from ai.utils.embedder import embedder
from ai.utils.database import TAG_CONTENT_NAME, TAG_ID_NAME, TAG_INDEX_NAME, TAG_UID_NAME, tag_collection
from ai.memo._models import Tag
from fastapi.concurrency import run_in_threadpool


async def retrieve_similar_tags(query: str, user_id: str) -> list[Tag]:
    tag_list: list[Tag]=await run_in_threadpool(_get_similar_tags_from_db, query, user_id)
    
    return tag_list

def _get_similar_tags_from_db(query: str, user_id: str) -> list[Tag]: 
    raw_tags=tag_collection.find({TAG_UID_NAME: user_id})
    raw_tags=tag_collection.aggregate([
        {
            "$vectorSearch": 
            {
                'index': TAG_INDEX_NAME,
                'path': "embedding",
                'queryVector': embedder.embed_query(query),
                'numCandidates': 1000,
                'limit': 30,
                'filter': { TAG_UID_NAME: user_id }
            }
        },
        {
            "$project": 
            {
                "_id": 1,
                TAG_CONTENT_NAME: 1,
            }
        },
    ])

    similar_tags: list[Tag]=[]
    
    for res in raw_tags:
        similar_tags.append(Tag(
            id=str(res[TAG_ID_NAME]),
            name=res[TAG_CONTENT_NAME],
            is_new=False
        ))
    return similar_tags

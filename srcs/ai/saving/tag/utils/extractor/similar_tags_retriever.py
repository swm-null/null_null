from ai.saving.tag.utils.tag_formatter import format_tags
from ai.utils.embedder import embedder
from ai.database.collections.tag_store import TAG_CONTENT_NAME, TAG_ID_NAME, TAG_INDEX_NAME, TAG_UID_NAME, tag_collection
from ai.saving.tag.models import Tag


def retrieve_similar_tags(query: str, user_id: str) -> str:
    tag_list: list[Tag]=_get_similar_tags_from_db(query, user_id)
    formatted_tag_list=format_tags(tag_list)
    return formatted_tag_list

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
            }
        },
        {
            "$project": 
            {
                "_id": 1,
                TAG_CONTENT_NAME: 1,
            }
        },
        {
            "$match":
            {
                "$expr": { TAG_UID_NAME: user_id}
            }
        }
    ])

    similar_tags: list[Tag]=[]
    
    for res in raw_tags:
        similar_tags.append(Tag(
            id=str(res[TAG_ID_NAME]),
            name=res[TAG_CONTENT_NAME],
        ))
    return similar_tags

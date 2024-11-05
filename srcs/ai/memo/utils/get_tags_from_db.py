from ai.memo._models.tag import Tag
from ai.utils.database import tag_collection, TAG_UID_NAME, TAG_ID_NAME, TAG_CONTENT_NAME


def get_tags_from_db(user_id: str) -> list[Tag]:
    raw_tags=tag_collection.find({TAG_UID_NAME: user_id})
    tags: list[Tag]=[]
    
    for res in raw_tags:
        tags.append(Tag(
            id=str(res[TAG_ID_NAME]),
            name=res[TAG_CONTENT_NAME],
            is_new=False
        ))
    
    return tags

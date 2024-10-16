from ai.database.collections.tag_store import tag_collection, TAG_UID_NAME, TAG_ID_NAME, TAG_CONTENT_NAME, TAG_ROOT_NAME


def get_tag_dict(user_id: str) -> tuple[dict[str, str], dict[str, str]]:
    tag_id_to_name, tag_name_to_id=_get_tags_from_db(user_id)
    
    return tag_id_to_name, tag_name_to_id
    
def _get_tags_from_db(user_id: str) -> tuple[dict[str, str], dict[str, str]]:
    id_to_name: dict[str, str]={}
    name_to_id: dict[str, str]={}
    raw_tags=tag_collection.find({TAG_UID_NAME: user_id})
    
    for raw_tag in raw_tags:
        id_to_name[raw_tag[TAG_ID_NAME]]=raw_tag[TAG_CONTENT_NAME]
        name_to_id[raw_tag[TAG_CONTENT_NAME]]=raw_tag[TAG_ID_NAME]
    
    return id_to_name, name_to_id

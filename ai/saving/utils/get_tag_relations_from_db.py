from ai.database.collections.tag_edges import tag_edges_collection, UID_FIELD_NAME


def get_tag_relations_from_db(user_id: str) -> dict[str, list[str]]:
    document=tag_edges_collection.find_one({UID_FIELD_NAME: user_id})
    
    if document:
        edges=document.get("edges")
        return edges
    return {}
    

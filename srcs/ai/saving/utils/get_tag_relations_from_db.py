from collections import defaultdict
from ai.database.collections.tag_edges import tag_edges_collection, UID_FIELD_NAME


def get_tag_relations_from_db(user_id: str) -> defaultdict[str, list[str]]:
    document=tag_edges_collection.find_one({UID_FIELD_NAME: user_id})
    
    if document:
        raw_edges: defaultdict[str, list[str]]=document.get("edges")
        return defaultdict(list[str], raw_edges)

    return defaultdict(list[str])
    

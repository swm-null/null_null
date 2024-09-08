from ai.saving.utils.get_tag_relations_from_db import get_tag_relations_from_db
from ai.database.collections.tag_store import tag_collection, TAG_UID_NAME, TAG_ID_NAME, TAG_CONTENT_NAME, TAG_ROOT_NAME


def get_formatted_directories(user_id: str) -> str:
    tag_id_to_name, tag_name_to_id=_get_tags_from_db(user_id)
    graph: dict[str, list[str]]=get_tag_relations_from_db(user_id)
    
    return _format_graph(graph, tag_id_to_name, tag_name_to_id[TAG_ROOT_NAME])

def _get_tags_from_db(user_id: str) -> tuple[dict[str, str], dict[str, str]]:
    id_to_name: dict[str, str]={}
    name_to_id: dict[str, str]={}
    raw_tags=tag_collection.find({TAG_UID_NAME: user_id})
    
    for raw_tag in raw_tags:
        id_to_name[raw_tag[TAG_ID_NAME]]=raw_tag[TAG_CONTENT_NAME]
        name_to_id[raw_tag[TAG_CONTENT_NAME]]=raw_tag[TAG_ID_NAME]
    
    return id_to_name, name_to_id
    
def _format_graph(graph: dict[str, list[str]], tag_id_to_name: dict[str, str], now_id: str, depth: int=1) -> str:
    result: str=f'{tag_id_to_name[now_id]} ({now_id})\n'
    next_ids: list[str]=_get_next_ids_from_graph(graph, now_id)
    
    for next_id in next_ids:
        result+=("-"*depth)+_format_graph(graph, tag_id_to_name, next_id, depth+1)
    
    return result

def _get_next_ids_from_graph(graph: dict[str, list[str]], now: str) -> list[str]:
        return graph[now] if now in graph else []
            

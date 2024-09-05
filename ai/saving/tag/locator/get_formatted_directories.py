from ai.saving.utils.get_tag_relations_from_db import get_tag_relations_from_db
from ai.database.collections.tag_store import tag_collection, TAG_UID_NAME, TAG_ID_NAME, TAG_CONTENT_NAME


def get_formatted_directories(user_id: str) -> str:
    graph: dict[str, list[str]]=get_tag_relations_from_db(user_id)
    tag_id_to_name: dict[str, str]=_get_tags_from_db(user_id)
    
    return _format_graph(graph, tag_id_to_name)

def _format_graph(graph: dict[str, list[str]], tag_id_to_name: dict[str, str], now: str="@", depth: int=0) -> str:
    result: str=""
    next_ids: list[str]=_get_next_ids_from_graph(graph, now)
    
    for next_id in next_ids:
        next_line: str="-"*depth 
        next_line+=f'{tag_id_to_name[next_id]} ({next_id})\n'
        next_result=_format_graph(graph, tag_id_to_name, next_id, depth+1)
        if next_result != "":
            next_line+=next_result
        
        result+=next_line
    
    return result

def _get_next_ids_from_graph(graph: dict[str, list[str]], now: str) -> list[str]:
        return graph[now] if now in graph else []
            
def _get_tags_from_db(user_id: str) -> dict[str, str]:
    tags: dict[str, str]={}
    raw_tags=tag_collection.find({TAG_UID_NAME: user_id})
    
    for raw_tag in raw_tags:
        tags[raw_tag[TAG_ID_NAME]]=raw_tag[TAG_CONTENT_NAME]
    
    return tags
    

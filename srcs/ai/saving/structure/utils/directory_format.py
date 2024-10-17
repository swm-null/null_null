from fastapi import HTTPException
from ai.saving.utils import aget_tag_relations_from_db
from ai.database.collections.tag_store import TAG_ROOT_NAME


async def get_formatted_directories(user_id: str, tag_id_to_name: dict[str, str], tag_name_to_id: dict[str, str]) -> str:
    graph: dict[str, list[str]]=await aget_tag_relations_from_db(user_id)
    if TAG_ROOT_NAME not in tag_name_to_id:
        raise HTTPException(status_code=500, headers={"/memo/structures": "root tag not found (@)"})
    
    return _format_graph(graph, tag_id_to_name, tag_name_to_id[TAG_ROOT_NAME])
    
def _format_graph(graph: dict[str, list[str]], tag_id_to_name: dict[str, str], now_id: str, depth: int=1) -> str:
    result: str=f'{tag_id_to_name[now_id]}\n'
    next_ids: list[str]=_get_next_ids_from_graph(graph, now_id)
    
    for next_id in next_ids:
        result+=("-"*depth)+_format_graph(graph, tag_id_to_name, next_id, depth+1)
    
    return result

def _get_next_ids_from_graph(graph: dict[str, list[str]], now: str) -> list[str]:
        return graph[now] if now in graph else []
            

from collections import defaultdict
from fastapi import HTTPException
from ai.memo.structure.utils.get_tag_relations_from_db import get_tag_relations_from_db
from ai.utils.database import TAG_ROOT_NAME


async def get_structure_dict(user_id: str, tag_id_to_name: dict[str, str], tag_name_to_id: dict[str, str]) -> dict[str, list[str]]:
    graph: dict[str, list[str]]=await get_tag_relations_from_db(user_id)
    if TAG_ROOT_NAME not in tag_name_to_id:
        raise HTTPException(status_code=500, headers={"/memo/structures": "root tag not found (@)"})
    
    structure_dict: defaultdict[str, list[str]]=defaultdict(list[str])
    _get_structure(graph, structure_dict, tag_id_to_name, tag_name_to_id[TAG_ROOT_NAME])
    
    return structure_dict
    
def _get_structure(graph: dict[str, list[str]], structure_dict: defaultdict[str, list[str]], tag_id_to_name: dict[str, str], now_id: str) -> None:
    now_name=tag_id_to_name[now_id]
    next_ids: list[str]=_get_next_ids_from_graph(graph, now_id)
    if not next_ids:
            return
    
    for next_id in next_ids:
        next_name=tag_id_to_name[next_id]
        structure_dict[now_name].append(next_name)
        _get_structure(graph, structure_dict, tag_id_to_name, next_id)

def _get_next_ids_from_graph(graph: dict[str, list[str]], now: str) -> list[str]:
        return graph[now] if now in graph else []
            

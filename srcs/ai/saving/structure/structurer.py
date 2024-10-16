from collections import defaultdict
from ai.saving.utils import get_tag_relations_from_db
from models.memo import Memo_tag_relation


def get_structure(user_id: str, relations: list[Memo_tag_relation]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    graph: defaultdict[str, list[str]]=get_tag_relations_from_db(user_id)
    for relation in relations:
        graph[relation.parent_id].append(relation.child_id)
    
    reversed_graph: defaultdict[str, list[str]]=defaultdict()
    for parent, childs in graph.items():
        for child in childs:
            reversed_graph[child].append(parent)
    
    return graph, reversed_graph

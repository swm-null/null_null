from models.memos import Memos_processed_memo, Memos_relations
from ai.saving.utils.get_tag_relations_from_db import get_tag_relations_from_db


def memos_structurer(processed_memos: list[Memos_processed_memo], user_id: str):
    graph: dict[str, list[str]]=get_tag_relations_from_db(user_id)
    for memo in processed_memos:
        _structurer(graph, memo.tags_relations)
    
    return graph

def memo_structurer(processed_memo: Memos_processed_memo, user_id: str):
    return memos_structurer([processed_memo], user_id)

def _structurer(graph: dict[str, list[str]], relations: Memos_relations) -> None:
    for relation in relations.added:
        graph[relation.parent_id].append(relation.child_id)
     
    for relation in relations.deleted:
        graph[relation.parent_id].remove(relation.child_id)
        if len(graph[relation.parent_id])==0:
            graph.pop(relation.parent_id)

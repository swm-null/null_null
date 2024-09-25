from collections import defaultdict
import logging
from models.memos_deprecated import Memo_processed_memo, Memo_relations
from ai.saving.utils import get_tag_relations_from_db


def memos_structurer(processed_memos: list[Memo_processed_memo], user_id: str):
    graph: defaultdict[str, list[str]]=get_tag_relations_from_db(user_id)
    for memo in processed_memos:
        _structurer(graph, memo.tags_relations)
    logging.info("[memos_structurer]\n## new structure:\n%s\n\n", graph)

    return graph

def memo_structurer(processed_memo: Memo_processed_memo, user_id: str):
    return memos_structurer([processed_memo], user_id)

def _structurer(graph: defaultdict[str, list[str]], relations: Memo_relations) -> None:
    for relation in relations.added:
        graph[relation.parent_id].append(relation.child_id)
     
    for relation in relations.deleted:
        graph[relation.parent_id].remove(relation.child_id)
        if len(graph[relation.parent_id])==0:
            graph.pop(relation.parent_id)

from ai.memo.structure._models.directory_relation import Directory_relation
from routers._models import Memo_tag_relation


def convert_relations(relations: list[Directory_relation]) -> list[Memo_tag_relation]:
    return [
        Memo_tag_relation(
            parent_id=relation.parent_id,
            child_id=relation.child_id
        ) for relation in relations
    ]

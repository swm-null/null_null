from datetime import datetime
import logging
from ai.saving.tag_deprecated.single import get_tag_single
from ai.utils import embedder
from models.memo import *

# deprecated
def single_processor(memo: Memo_raw_memo, user_id: str, lang: str="Korean") -> Memo_processed_memo:
    new_tag_list, parent_tags, dir_relations=get_tag_single(memo.content, user_id, lang)
    logging.info("[single_processor]\n## new_tag_list:\n%s\n\n## parent_tags:\n%s\n\n## dir_relations:\n%s\n\n", new_tag_list, parent_tags, dir_relations)

    new_tags: list[Memo_tag]=[
        Memo_tag(
            embedding=embedder.embed_query(tag.name),
            name=tag.name, 
            id=tag.id
        ) for tag in new_tag_list
    ]
    
    parent_tag_ids: list[str]=[
        parent.id for parent in parent_tags
    ]
    
    tag_relations: list[Memo_tag_relation]=[
        Memo_tag_relation(
            parent_id=relation.parent_id,
            child_id=relation.child_id,
        ) for relation in dir_relations
    ]
    
    return Memo_processed_memo(
        content=memo.content,
        timestamp=datetime.now() if memo.timestamp is None else memo.timestamp,
        parent_tag_ids=parent_tag_ids,
        tags_relations=Memo_relations(
            added=tag_relations,
            deleted=[]
        ),
        new_tags=new_tags,
        embedding=embedder.embed_query(memo.content),
    )

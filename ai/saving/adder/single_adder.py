from datetime import datetime
import logging
from ai.saving import query_extractor as qe
from ai.saving.tag.single import get_tag_single
from ai.utils.embedder import embedder
from models.add_memo import Arg_add_memo, Res_add_memo, Res_memo_tag
from models.memos import *

def single_adder(memo: Memos_raw_memo, user_id: str, lang: str="Korean") -> Memos_processed_memo:
    new_tag_list, parent_tags, dir_relations=get_tag_single(memo.content, user_id, lang)
    logging.info("[single_adder]\n## new_tag_list:\n%s\n\n## parent_tags:\n%s\n\n## dir_relations:\n%s\n\n", new_tag_list, parent_tags, dir_relations)

    new_tags: list[Memos_tag]=[
        Memos_tag(
            embedding=embedder.embed_query(tag.name),
            name=tag.name, 
            id=tag.id
        ) for tag in new_tag_list
    ]
    
    parent_tag_ids: list[str]=[
        parent.id for parent in parent_tags
    ]
    
    tag_relations: list[Memos_tag_relation]=[
        Memos_tag_relation(
            parent_id=relation.parent_id,
            child_id=relation.child_id,
        ) for relation in dir_relations
    ]
    
    return Memos_processed_memo(
        content=memo.content,
        timestamp=datetime.now() if memo.timestamp is None else memo.timestamp,
        parent_tag_ids=parent_tag_ids,
        tag_relations=Memos_relations(
            added=tag_relations,
            deleted=[]
        ),
        new_tags=new_tags,
        embedding=embedder.embed_query(memo.content),
    )

def single_adder_deprecated(memo: Arg_add_memo) -> Res_add_memo:
    existing_tag_ids: list[str]
    new_tags: list[Res_memo_tag]
    existing_tag_ids, new_tags = qe.query_extractor(memo.content)

    return Res_add_memo(
        content=memo.content,
        existing_tag_ids=existing_tag_ids,
        new_tags=new_tags,
        timestamp=datetime.now() if memo.timestamp is None else memo.timestamp,
        memo_embeddings=embedder.embed_query(memo.content),
    )

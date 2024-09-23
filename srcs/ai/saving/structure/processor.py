import asyncio
from typing import Optional
from models.memo_structures import Memos_memo_and_tags, Memos_processed_memo
from ai.saving.structure.models import Tag, Memo
from ai.saving.structure.utils.memo_and_tags_converter import convert_memos_and_tags
from ai.saving.structure.utils.locator.tag_locator import locate_tags
from ai.saving.structure.models.directory_relation import Directory_relation
from ai.utils import embedder
from models.memos import Memos_tag, Memos_tag_relation


async def process_memos(user_id: str, memos_and_tags: list[Memos_memo_and_tags], lang: str="Korean") -> tuple[list[Memos_processed_memo], list[Memos_tag_relation], list[Memos_tag]]:
    located_memos_and_tags, relations, located_tags=_locate_memos(user_id, memos_and_tags, lang)
    
    process_memo_tasks=[_process_memo(memo_and_tags) for memo_and_tags in located_memos_and_tags]
    processed_memos=await asyncio.gather(*process_memo_tasks)
    
    converted_relations=_convert_relations(relations)
    
    process_tag_tasks=[_convert_tag(tag) for tag in located_tags]
    converted_tags=await asyncio.gather(*process_tag_tasks)
     
    return processed_memos, converted_relations, converted_tags

async def _process_memo(memo_and_tags: Memo) -> Memos_processed_memo:
    return Memos_processed_memo(
            content=memo_and_tags.content,
            parent_tag_ids=memo_and_tags.parent_tag_ids,
            timestamp=memo_and_tags.timestamp,
            embedding=await embedder.aembed_query(memo_and_tags.content)
    )
    
def _convert_relations(relations: list[Directory_relation]) -> list[Memos_tag_relation]:
    return [
        Memos_tag_relation(
            parent_id=relation.parent_id,
            child_id=relation.child_id
        ) for relation in relations
    ]  

async def _convert_tag(tag: Tag) -> Memos_tag:
    return Memos_tag(
        name=tag.name,
        id=tag.id,
        embedding=await embedder.aembed_query(tag.name)
    )

def _locate_memos(user_id: str, memos_and_tags: list[Memos_memo_and_tags], lang: str) -> tuple[list[Memo], list[Directory_relation], list[Tag]]:
    memos, tags=convert_memos_and_tags(memos_and_tags)
    new_tags: list[Tag]=_get_new_tags(tags)
    
    relations, located_tags=locate_tags(user_id, new_tags, lang)
    located_and_merged_tags=_merge_located_tags_and_new_tags(located_tags, new_tags)
    located_memos_and_tags: list[Memo]=_link_memos_and_tags(memos, located_and_merged_tags)
    
    return located_memos_and_tags, relations, located_and_merged_tags
        
def _get_new_tags(tags: list[Tag]) -> list[Tag]:
    return [tag for tag in tags if tag.is_new]

def _merge_located_tags_and_new_tags(located_tags: list[Tag], new_tags: list[Tag]) -> list[Tag]:
    tag_name_to_original_tag: dict[str, tuple[str, Optional[int]]]={tag.name: (tag.id, tag.connected_memo_id) for tag in new_tags}
    
    return [
        Tag(
            id=tag_name_to_original_tag[tag.name][0] if tag.name in tag_name_to_original_tag else tag.id,
            name=tag.name,
            is_new=tag.is_new,
            connected_memo_id=tag_name_to_original_tag[tag.name][1] if tag.name in tag_name_to_original_tag else tag.connected_memo_id
        ) for tag in located_tags
    ]

def _link_memos_and_tags(memos: dict[int, Memo], tags: list[Tag]) -> list[Memo]:
    linked_memo_id_to_tags: dict[int, list[Tag]]=dict()
    
    for tag in tags:
        if tag.connected_memo_id:
            linked_memo_id_to_tags.setdefault(tag.connected_memo_id, []).append(tag)
    
    linked_memos: list[Memo]=[
        Memo(
            content=memo.content,
            parent_tag_ids=[tag.id for tag in linked_memo_id_to_tags[memo_id]],
            timestamp=memo.timestamp
        ) for memo_id, memo in memos.items()
    ]
    
    return linked_memos
        

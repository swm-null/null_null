import asyncio
from collections import defaultdict
from typing import Optional
from models.memo import Memo_memo_and_tags, Memo_processed_memo
from ai.saving._models import Tag
from ai.saving.structure._models import Memo
from ai.saving.structure.utils import convert_tag, convert_relations, convert_memos_and_tags, extract_and_assign_metadata
from ai.saving.structure.utils.locator.tag_locator import locate_tags
from ai.saving.structure._models.directory_relation import Directory_relation
from models.memo import Memo_tag, Memo_tag_relation
from ai.utils import embedder


async def process_memos(user_id: str, memos_and_tags: list[Memo_memo_and_tags], lang: str="Korean") -> tuple[list[Memo_processed_memo], list[Memo_tag_relation], list[Memo_tag]]:
    memos, tags=convert_memos_and_tags(memos_and_tags)
    memos_with_metadata=await extract_and_assign_metadata(memos, lang)
    located_memos_and_tags, relations, located_tags=_locate_memos(user_id, memos_with_metadata, tags, lang)
    
    process_memo_tasks=[_process_memo(memo_and_tags) for memo_and_tags in located_memos_and_tags]
    processed_memos=await asyncio.gather(*process_memo_tasks)
    
    converted_relations=convert_relations(relations)
    
    process_tag_tasks=[convert_tag(tag) for tag in located_tags]
    converted_tags=await asyncio.gather(*process_tag_tasks)
     
    return processed_memos, converted_relations, converted_tags

async def _process_memo(memo_and_tags: Memo) -> Memo_processed_memo:
    return Memo_processed_memo(
            content=memo_and_tags.content,
            image_urls=memo_and_tags.image_urls,
            metadata=str(memo_and_tags.metadata),
            parent_tag_ids=memo_and_tags.parent_tag_ids,
            timestamp=memo_and_tags.timestamp,
            embedding=await embedder.aembed_query(memo_and_tags.content)
    )
    
def _locate_memos(user_id: str, memos: dict[int, Memo], tags: list[Tag], lang: str) -> tuple[list[Memo], list[Directory_relation], list[Tag]]:
    new_tags, exist_tags=_categorize_tags(tags)
    
    relations, located_tags=locate_tags(user_id, new_tags, memos, lang)
    located_and_merged_tags=_merge_located_tags_and_new_tags(located_tags, new_tags)
    merged_relations=_merge_relations_and_new_tags(relations, new_tags)
    located_memos_and_tags: list[Memo]=_link_memos_and_tags(memos, located_and_merged_tags+exist_tags)
    
    return located_memos_and_tags, merged_relations, located_and_merged_tags
        
def _categorize_tags(tags: list[Tag]) -> tuple[list[Tag], list[Tag]]:
    return [tag for tag in tags if tag.is_new], [tag for tag in tags if not tag.is_new]

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

def _merge_relations_and_new_tags(relations: list[Directory_relation], new_tags: list[Tag]) -> list[Directory_relation]:
    tag_name_to_original_tag_id: dict[str, str]={tag.name: tag.id for tag in new_tags}
    
    return [
        Directory_relation(
            parent_id=tag_name_to_original_tag_id[relation.parent_name] if relation.parent_name in tag_name_to_original_tag_id else relation.parent_id,
            parent_name=relation.parent_name,
            child_id=tag_name_to_original_tag_id[relation.child_name] if relation.child_name in tag_name_to_original_tag_id else relation.child_id,
            child_name=relation.child_name
        ) for relation in relations
    ]
    
def _link_memos_and_tags(memos: dict[int, Memo], tags: list[Tag]) -> list[Memo]:
    linked_memo_id_to_tags: defaultdict[int, list[Tag]]=defaultdict(list[Tag])

    for tag in tags:
        if tag.connected_memo_id:
            linked_memo_id_to_tags[tag.connected_memo_id].append(tag)
    
    linked_memos: list[Memo]=[
        Memo(
            content=memo.content,
            image_urls=memo.image_urls,
            metadata=memo.metadata,
            parent_tag_ids=[tag.id for tag in linked_memo_id_to_tags[memo_id]],
            timestamp=memo.timestamp
        ) for memo_id, memo in memos.items()
    ]
    
    return linked_memos
        

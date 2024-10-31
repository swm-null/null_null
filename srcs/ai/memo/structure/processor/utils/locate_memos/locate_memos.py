from collections import defaultdict
from typing import Optional
from ai.memo._models.tag import Tag
from ai.memo.structure.processor._models import Memo, Directory_relation
from ai.memo.structure.processor.utils.locate_memos.utils import get_tag_dict, locate_tags


async def locate_memos(user_id: str, memos: dict[int, Memo], tags: list[Tag], lang: str) -> tuple[list[Memo], list[Directory_relation], list[Tag]]:
    new_given_tags, existing_tags=await _categorize_new_tags_and_existing_tags(user_id, tags)
    new_relations, new_created_tags=await locate_tags(user_id, new_given_tags, memos, lang)
    
    merged_tags=_merge_new_created_tags_and_new_tags(new_created_tags, new_given_tags)
    merged_relations=_merge_relations_and_new_tags(new_relations, new_given_tags)
    
    located_memos_and_tags: list[Memo]=_link_memos_and_tags(memos, merged_tags+existing_tags)
    
    return located_memos_and_tags, merged_relations, merged_tags
        
async def _categorize_new_tags_and_existing_tags(user_id: str, tags: list[Tag]) -> tuple[list[Tag], list[Tag]]:
    _, tag_name_to_id=await get_tag_dict(user_id)
    
    new_tags: list[Tag]=[
        Tag(
            id=tag.id,
            name=tag.name,
            is_new=True,
            connected_memo_id=tag.connected_memo_id
        ) for tag in tags if tag.name not in tag_name_to_id
    ]
    existing_tags: dict[str, Tag]={
        tag.name: Tag(
            id=tag_name_to_id[tag.name],
            name=tag.name,
            is_new=False,
            connected_memo_id=tag.connected_memo_id
        ) for tag in tags if tag.name in tag_name_to_id
    }
    
    return new_tags, list(existing_tags.values())

def _merge_new_created_tags_and_new_tags(new_created_tags: list[Tag], new_tags: list[Tag]) -> list[Tag]:
    tag_name_to_original_tag: dict[str, tuple[str, Optional[int]]]={tag.name: (tag.id, tag.connected_memo_id) for tag in new_tags}
    
    return [
        Tag(
            id=tag_name_to_original_tag[tag.name][0] if tag.name in tag_name_to_original_tag else tag.id,
            name=tag.name,
            is_new=tag.is_new,
            connected_memo_id=tag_name_to_original_tag[tag.name][1] if tag.name in tag_name_to_original_tag else tag.connected_memo_id
        ) for tag in new_created_tags
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
            record_urls=memo.record_urls,
            metadata=memo.metadata,
            parent_tag_ids=[tag.id for tag in linked_memo_id_to_tags[memo_id]],
            timestamp=memo.timestamp
        ) for memo_id, memo in memos.items()
    ]
    
    return linked_memos
        

import logging
import uuid
from ai.saving._models import Tag
from ai.saving.structure._models.directory_relation import Directory_relation
from ai.saving.structure.utils.directory_format import get_formatted_directories
from ai.saving.structure.utils.locator.chains import get_new_relations_and_tags_chain
from ai.saving.structure.utils.locator.chains.get_new_relations_and_tags_chain import Relation_for_chain
from ai.saving.structure.utils.locator.chains.get_new_relations_and_tags_chain import get_new_relations_and_tags_chain, Get_new_relations_and_tags_chain_output
from ai.saving.structure._models.memo import Memo
from ai.saving.structure.utils import get_tag_dict


async def locate_tags(user_id: str, tags: list[Tag], memos: dict[int, Memo], lang: str) -> tuple[list[Directory_relation], list[Tag]]:
    tag_id_to_name, tag_name_to_id=await get_tag_dict(user_id)
    formatted_directories: str=await get_formatted_directories(user_id, tag_id_to_name, tag_name_to_id)
    new_dir_relations, new_tags=_get_new_relations_and_tags(tags, memos, lang, formatted_directories, tag_name_to_id)
    logging.info("[locate_tags]\n## new_dir_relations:\n%s\n\n## new tags:\n%s\n\n", new_dir_relations, new_tags)
    
    return new_dir_relations, new_tags

def _format_tags(tags: list[Tag]) -> str:
    return ", ".join(f"\"{tag.name}\" for memo {tag.connected_memo_id}" for tag in tags)

def _format_metadatas(memos: dict[int, Memo]) -> str:
    return "".join(f"\nmemo {id}: \"{memo.metadata}\"" for id, memo in memos.items())
    
def _get_new_relations_and_tags(tags: list[Tag], memos: dict[int, Memo], lang:str, directories: str, tag_name_to_id: dict[str, str]) -> tuple[list[Directory_relation], list[Tag]]:
    chain_result: Get_new_relations_and_tags_chain_output=get_new_relations_and_tags_chain.invoke({"tags": _format_tags(tags), "metadatas": _format_metadatas(memos), "lang": lang, "directories": directories})
    tag_name_to_tag: dict[str, Tag]=_assign_id_to_new_tags(chain_result.new_directories)
    merged_tag_name_to_id: dict[str, str]=_merge_new_tag_ids_and_existing_tag_ids(tag_name_to_tag, tag_name_to_id)
    modified_relations: list[Directory_relation]=_modify_id_on_new_relations(chain_result.relations, merged_tag_name_to_id)
    
    return modified_relations, [*tag_name_to_tag.values()]

def _assign_id_to_new_tags(tag_names: list[str]) -> dict[str, Tag]:
    tag_name_to_tag: dict[str, Tag]={}
    
    for tag_name in tag_names:
        tag_name_to_tag[tag_name]=Tag(
            id=uuid.uuid4().hex,
            name=tag_name,
            is_new=True
        )
    
    return tag_name_to_tag

def _merge_new_tag_ids_and_existing_tag_ids(new_tags: dict[str, Tag], existing_tag_name_to_id: dict[str, str]) -> dict[str, str]:
    merged: dict[str, str]={}
    
    for new_tag in new_tags.values():
        merged[new_tag.name]=new_tag.id
    merged.update(existing_tag_name_to_id)
    
    return merged

def _modify_id_on_new_relations(relations: list[Relation_for_chain], tag_name_to_id: dict[str, str]) -> list[Directory_relation]:
    return [
        Directory_relation(
            parent_name=relation.parent_name,
            parent_id=tag_name_to_id[relation.parent_name],
            child_name=relation.child_name,
            child_id=tag_name_to_id[relation.child_name],
        ) for relation in relations
    ]
    

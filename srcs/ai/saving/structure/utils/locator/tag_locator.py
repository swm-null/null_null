import uuid
from ai.saving.structure._models import Tag
from ai.saving.structure._models.directory_relation import Directory_relation
from ai.saving.structure.utils.directory_format import get_formatted_directories
from ai.saving.structure.utils.locator.chains import get_new_relations_and_tags_chain
from ai.saving.structure.utils.locator.chains.get_new_relations_and_tags_chain import get_new_relations_and_tags_chain, Get_new_relations_and_tags_chain_output


def locate_tags(user_id: str, tags: list[Tag], lang: str) -> tuple[list[Directory_relation], list[Tag]]:
    formatted_directories: str=get_formatted_directories(user_id)
    new_dir_relations, new_tags=_get_new_relations_and_tags(tags, lang, formatted_directories)
    
    return new_dir_relations, new_tags

def _format_tags(tags: list[Tag]) -> str:
    return ", ".join(tag.name for tag in tags)

def _get_new_relations_and_tags(tags: list[Tag], lang:str, directories: str) -> tuple[list[Directory_relation], list[Tag]]:
    chain_result: Get_new_relations_and_tags_chain_output=get_new_relations_and_tags_chain.invoke({"tags": _format_tags(tags), "lang": lang, "directories": directories})
    tag_name_to_tag: dict[str, Tag]=_assign_id_to_new_tags(chain_result.new_directories)
    modified_relations: list[Directory_relation]=_modify_id_on_new_relations(chain_result.relations, tag_name_to_tag)
    
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

def _modify_id_on_new_relations(relations: list[Directory_relation], tag_name_to_tag: dict[str, Tag]) -> list[Directory_relation]:
    return [
        Directory_relation(
            parent_name=relation.parent_name,
            parent_id=tag_name_to_tag[relation.parent_name].id if relation.parent_id in tag_name_to_tag else relation.parent_id,
            child_name=relation.child_name,
            child_id=tag_name_to_tag[relation.child_name].id if relation.child_id in tag_name_to_tag else relation.child_id,
        ) for relation in relations
    ]
    

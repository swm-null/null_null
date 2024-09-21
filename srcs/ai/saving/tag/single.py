from ai.saving.tag.models import Directory_relation, Tag
from ai.saving.tag.extractor import tag_extractor
from ai.saving.tag.locator import tag_locator
from ai.saving.tag.selector import tag_selector


def get_tag_single(query: str, user_id: str, lang: str="Korean") -> tuple[list[Tag], list[Tag], list[Directory_relation]]:
    candidate_tag_list=tag_extractor(query, user_id, lang)
    selected_tag_list=tag_selector(query, candidate_tag_list, lang)
    
    new_tag_list: list[Tag]=[]
    parent_tags: list[Tag]=[]
    dir_relations: list[Directory_relation]=[]
    
    for tag in selected_tag_list:
        if tag.id == tag.name: # is newly created tag
            new_directory_relations, new_directories=_add_new_tag(tag, user_id, lang)
            dir_relations.extend(new_directory_relations)
            new_tag_list.extend(new_directories)

        parent_tags.append(tag)
        
    _assign_new_tags_id(new_tag_list, parent_tags, dir_relations)
    
    return new_tag_list, parent_tags, dir_relations
                    
def _add_new_tag(tag: Tag, user_id: str, lang: str="Korean") -> tuple[list[Directory_relation], list[Tag]]:
    new_directory_relations: list[Directory_relation]=tag_locator(tag.name, user_id, lang)
    new_directories: list[Tag]=_process_new_directories(new_directory_relations)
    
    return new_directory_relations, new_directories
    
def _process_new_directories(relations: list[Directory_relation]) -> list[Tag]:
    new_directories: list[Tag]=[]
    
    for relation in relations:
        if relation.is_new:
            new_directories.append(
                Tag(
                    name=relation.child_name,
                    id=relation.child_id,
                )
            )
    
    return new_directories
    
def _assign_new_tags_id(new_tag_list: list[Tag], parent_tags: list[Tag], dir_relations: list[Directory_relation]) -> None:
    new_tag_dict: dict[str, str]={new_tag.name: new_tag.id for new_tag in new_tag_list}
    
    for tag in parent_tags:
        if tag.id in new_tag_dict:
            tag.id=new_tag_dict[tag.id]
    
    for relation in dir_relations:
        if relation.child_id in new_tag_dict:
            relation.child_id=new_tag_dict[relation.child_id]
        
    for relation in dir_relations:
        if relation.parent_id in new_tag_dict:
            relation.parent_id=new_tag_dict[relation.parent_id]

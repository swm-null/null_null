import logging
import uuid
from ai.saving.tag.models import Directory_relation
from ai.saving.tag.locator.chains.get_new_relations_chain import get_new_relations_chain
from ai.saving.tag.locator.get_formatted_directories import get_formatted_directories

    
def tag_locator(name: str, user_id: str, lang: str="Korean") -> list[Directory_relation]:
    formatted_directories: str=get_formatted_directories(user_id)
    new_dir_relations: list[Directory_relation]=_get_new_relations(name, lang, formatted_directories)
    logging.info("[tag_locator]\n## formatted directories:\n%s\n\n## new_dir_relations:\n%s\n\n", formatted_directories, new_dir_relations)
    
    return new_dir_relations

def _get_new_relations(name: str, lang: str, directories: str) -> list[Directory_relation]:
    chain_result=get_new_relations_chain.invoke({"name": name, "lang": lang, "directories": directories})
    logging.info("[_get_new_relations]\n## chain result:\n%s\n\n", chain_result)
    _assign_directories_id(chain_result.new_directories)
    
    return chain_result.new_directories

def _assign_directories_id(new_relations: list[Directory_relation]) -> None:    
    for relation in new_relations:
        if relation.is_new:
            relation.child_id=uuid.uuid4().hex
        
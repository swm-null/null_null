import logging
from ai.memo._models import Tag
from ai.memo.tag.utils.selector.chains import select_tag


async def select_tags(query: str, tags: list[Tag], lang: str="Korean") -> list[Tag]:
    chain_result=await select_tag(query, tags, lang)
    uniqued_tags: list[Tag]=_get_uniqued_tags(chain_result.tag_names, tags)
    logging.info("[select_tags]\n## selected tags:\n%s\n\n", uniqued_tags)
    
    return uniqued_tags

def _get_uniqued_tags(selected_tag_names: list[str], tags: list[Tag]) -> list[Tag]:
    tag_dict: dict[str, Tag]={tag.name: tag for tag in tags}
    
    return [tag_dict[tag_name] for tag_name in selected_tag_names]

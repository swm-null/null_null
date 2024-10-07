from collections import defaultdict
import logging
from ai.saving._models import Tag
from ai.saving.tag.utils.selector.chains import tag_selector_chain


async def select_tags(query: str, tag_list: list[Tag], lang: str="Korean") -> list[Tag]:
    chain_result=await tag_selector_chain.ainvoke({"query": query, "tag_list": tag_list, "lang": lang})
    uniqued_tags: list[Tag]=_get_uniqued_tags(chain_result.tag_list)
    logging.info("[select_tags]\n## selected tags:\n%s\n\n", uniqued_tags)
    
    return uniqued_tags

def _get_uniqued_tags(tags: list[Tag]) -> list[Tag]:
    tag_dict=defaultdict(list[Tag])
    
    for tag in tags:
        tag_dict[tag.name].append(tag)
    
    uniqued_tags: list[Tag]=[]
    for name, tags in tag_dict.items():
        merged=tags[0]
        for tag in tags:
            if tag.id != tag.name: 
                merged.id=tag.id
        uniqued_tags.append(merged)
    
    return uniqued_tags

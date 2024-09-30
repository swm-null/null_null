import logging
from ai.saving._models import Tag
from ai.saving.tag.utils.selector.chains import tag_selector_chain


async def select_tags(query: str, tag_list: list[Tag], lang: str="Korean") -> list[Tag]:
    chain_result=await tag_selector_chain.ainvoke({"query": query, "tag_list": tag_list, "lang": lang})
    logging.info("[select_tags]\n## selected tags:\n%s\n\n", chain_result)

    return chain_result.tag_list

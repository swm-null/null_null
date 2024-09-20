import logging
from ai.saving.tag.models import Tag
from ai.saving.tag.selector.chains import tag_selector_chain


# TODO: change to async func
def tag_selector(query: str, tag_list: list[Tag], lang: str="Korean") -> list[Tag]:
    chain_result=tag_selector_chain.invoke({"query": query, "tag_list": tag_list, "lang": lang})
    logging.info("[tag_selector]\n## selected tags:\n%s\n\n", chain_result)

    return chain_result.tag_list

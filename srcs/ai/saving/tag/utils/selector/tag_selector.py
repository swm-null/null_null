import logging
from ai.saving.tag._models import Tag
from ai.saving.tag.utils.selector.chains import tag_selector_chain


def select_tags(query: str, tag_list: list[Tag], lang: str="Korean") -> list[Tag]:
    chain_result=tag_selector_chain.invoke({"query": query, "tag_list": tag_list, "lang": lang})
    logging.info("[select_tags]\n## selected tags:\n%s\n\n", chain_result)

    return chain_result.tag_list

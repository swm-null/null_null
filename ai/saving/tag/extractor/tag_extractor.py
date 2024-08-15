import logging
from langchain_core.runnables import RunnableParallel
from ai.saving.tag.extractor.chains.existing_tag import existing_tag_chain
from ai.saving.tag.extractor.chains.new_tag import new_tag_chain
from ai.saving.tag._models.tag import Tag


def tag_extractor(query: str, user_lang: str="Korean") -> list[Tag]:
    chain=RunnableParallel(existing=existing_tag_chain, new=new_tag_chain)
    chain_result=chain.invoke({"query": query, "lang": user_lang})
    logging.info("[tag_extractor]\n## existing tags:\n%s\n\n## new tags:\n%s\n\n", chain_result["existing"].tag_list, chain_result["new"])
    
    extracted_tag: list[Tag]=[]
    
    extracted_tag.extend(chain_result["existing"].tag_list)
    extracted_tag.append(chain_result["new"]) # this tag's id should be tag's name
    
    return extracted_tag
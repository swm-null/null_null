import logging
from langchain_core.runnables import RunnableParallel
from ai.saving.tag.utils.extractor.chains import existing_tag_chain, new_tag_chain
from ai.saving._models import Tag


def extract_tags(query: str, user_id: str, lang: str="Korean") -> list[Tag]:
    chain=RunnableParallel(existing=existing_tag_chain, new=new_tag_chain)
    chain_result=chain.invoke({"query": query, "lang": lang, "user_id": user_id})
    logging.info("[extract_tags]\n## existing tags:\n%s\n\n## new tags:\n%s\n\n", chain_result["existing"].tag_list, chain_result["new"])
    
    extracted_tag: list[Tag]=[]
    
    extracted_tag.extend(chain_result["existing"].tag_list)
    if not any(exist_tag.name == chain_result["new"].name for exist_tag in chain_result["existing"].tag_list): 
        extracted_tag.append(chain_result["new"]) # this tag's id should be tag's name
    
    return extracted_tag

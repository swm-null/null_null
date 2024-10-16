import asyncio
import logging
from langchain_core.runnables import RunnableParallel
from ai.saving.tag.utils.extractor.chains import existing_tag_chain, new_tag_chain
from ai.saving.tag.utils.extractor.similar_tags_retriever import retrieve_similar_tags
from ai.saving.tag.utils.tag_formatter import format_tags
from ai.saving._models import Tag


async def extract_tags(query: str, user_id: str, lang: str="Korean") -> list[Tag]:
    similar_tags: list[Tag]=retrieve_similar_tags(query, user_id)
    chain=RunnableParallel(existing=existing_tag_chain, new=new_tag_chain)
    chain_result=await asyncio.create_task(chain.ainvoke({"query": query, "lang": lang, "user_id": user_id, "tag_names": format_tags(similar_tags)}))
    logging.info("[extract_tags]\n## existing tags:\n%s\n\n## new tags:\n%s\n\n", chain_result["existing"].tag_list, chain_result["new"].name)
    
    extracted_tags: list[Tag]=_convert_existing_chain_result(chain_result["existing"].tag_list, similar_tags)
    if not chain_result["new"].name in chain_result["existing"].tag_list:
        extracted_tags.extend(_convert_new_chain_result(chain_result["new"].name))
    logging.info("[extract_tags]\n## uniqued extracted tags:\n%s\n\n", extracted_tags)
    
    return extracted_tags

def _convert_existing_chain_result(selected_tag_names: list[str], tags: list[Tag]) -> list[Tag]:
    return [
        Tag(
            id=tag.id,
            name=tag.name,
            is_new=False
        )
        for tag in tags if tag.name in selected_tag_names
    ]

def _convert_new_chain_result(tag_name: str) -> list[Tag]:
    return [
        Tag(
            id=tag_name, 
            name=tag_name, 
            is_new=True
        )
    ]

import asyncio
import logging
from ai.memo.tag.utils.extractor.chains import get_existing_tag, get_new_tag
from ai.memo.tag.utils.extractor.utils import retrieve_similar_tags
from ai.memo._models import Tag


async def extract_tags(query: str, user_id: str, lang: str="Korean") -> list[Tag]:
    similar_tags: list[Tag]=retrieve_similar_tags(query, user_id)
    existing_candidtate_tags_chain_result, new_candidate_tag_chain_result=await asyncio.gather(
        get_existing_tag(query, similar_tags, lang),
        get_new_tag(query, lang)
    )
    logging.info("[extract_tags]\n## existing tags:\n%s\n\n## new tags:\n%s\n\n", existing_candidtate_tags_chain_result, new_candidate_tag_chain_result)
    
    extracted_tags: list[Tag]=_convert_existing_chain_result(existing_candidtate_tags_chain_result.tag_list, similar_tags)
    if not new_candidate_tag_chain_result.name in existing_candidtate_tags_chain_result.tag_list:
        extracted_tags.extend(_convert_new_chain_result(new_candidate_tag_chain_result.name))
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

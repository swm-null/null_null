import asyncio
import logging
from ai.memo.tag.deprecated.utils.extractor.chains import get_existing_tag, get_new_tag
from ai.memo.tag.deprecated.utils.extractor.utils import retrieve_similar_tags
from ai.memo._models import Tag


async def extract_tags(query: str, user_id: str, lang: str="Korean") -> list[Tag]:
    retrieved_similar_tags: list[Tag]=await retrieve_similar_tags(query, user_id)
    existing_candidtate_tags_chain_result, new_candidate_tag_chain_result=await asyncio.gather(
        get_existing_tag(query, retrieved_similar_tags, lang),
        get_new_tag(query, lang)
    )
    extracted_existing_tag_names: list[str]=existing_candidtate_tags_chain_result.tag_list
    _validate_and_fix_existing_tag_names(extracted_existing_tag_names, retrieved_similar_tags)
    extracted_new_tag_name: str=new_candidate_tag_chain_result.name
    logging.info("[extract_tags]\n## existing tags:\n%s\n\n## new tags:\n%s\n\n", extracted_existing_tag_names, extracted_new_tag_name)
    
    extracted_tags: list[Tag]=_get_uniqued_extracted_tags(extracted_existing_tag_names, extracted_new_tag_name, retrieved_similar_tags)
    logging.info("[extract_tags]\n## uniqued extracted tags:\n%s\n\n", extracted_tags)
    
    return extracted_tags

def _validate_and_fix_existing_tag_names(extracted_tag_names: list[str], retrieved_tags: list[Tag]):
    retrieved_tag_names: set[str]={tag.name for tag in retrieved_tags}
    extracted_tag_names[:]=[name for name in extracted_tag_names if name in retrieved_tag_names]
    
def _get_uniqued_extracted_tags(extracted_existing_tag_names: list[str], extracted_new_tag_name: str, original_tags: list[Tag]):
    extracted_tags: list[Tag]=_convert_existing_chain_result(extracted_existing_tag_names, original_tags)
    if not extracted_new_tag_name in extracted_existing_tag_names:
        extracted_tags.extend(_convert_new_chain_result(extracted_new_tag_name))
    
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

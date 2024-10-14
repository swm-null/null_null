import asyncio
import uuid
from models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.saving.tag.utils import extract_tags, select_tags
from ai.saving._models import Tag
from ai.saving.utils import is_new_tag
from ai.saving.utils.link_extractor import extract_link
from ai.saving.utils.image_converter import convert_image_to_content
from ai.saving.utils.link_converter import convert_link_to_content


async def create_tag(user_id: str, raw_memo: Memo_raw_memo, lang: str="Korean") -> list[Memo_tag_name_and_id]:
    await _process_metadata(raw_memo, lang)
    candidate_tags: list[Tag]=await extract_tags(raw_memo.content, user_id, lang)
    selected_tags: list[Tag]=await select_tags(raw_memo.content, candidate_tags, lang)
    assigned_tags: list[Memo_tag_name_and_id]=_assign_tags(selected_tags)
    
    return assigned_tags

async def _process_metadata(raw_memo: Memo_raw_memo, lang) -> None: 
    extracted_links: list[str]=extract_link(raw_memo.content)
    
    tasks=[]
    if raw_memo.image_urls:
        tasks.append(convert_image_to_content(raw_memo.image_urls, lang))
    if extracted_links:
        tasks.append(convert_link_to_content(extracted_links, lang))
    
    converted_contents: list[str]=await asyncio.gather(*tasks)    
    raw_memo.content+="\n"+"\n".join(converted_contents)
    
def _assign_tags(selected_tags: list[Tag]) -> list[Memo_tag_name_and_id]:
    return [
        Memo_tag_name_and_id(
            id=uuid.uuid4().hex if is_new_tag(selected_tag) else selected_tag.id,
            name=selected_tag.name,
            is_new=is_new_tag(selected_tag)
        ) for selected_tag in selected_tags
    ]

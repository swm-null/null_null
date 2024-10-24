import asyncio
import uuid
from routers._models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.memo.tag.utils import extract_tags, select_tags, is_new_tag
from ai.memo._models import Tag
from ai.memo.utils import extract_link, image_to_text, link_to_text


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
        tasks.append(asyncio.create_task(image_to_text(raw_memo.image_urls, lang)))
    if extracted_links:
        tasks.append(asyncio.create_task(link_to_text(extracted_links, lang)))
    
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

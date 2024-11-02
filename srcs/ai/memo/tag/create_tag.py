import asyncio
import uuid
from routers._models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.memo.tag.utils import extract_tags, select_tags, is_new_tag
from ai.memo._models import Tag
from ai.memo.utils import process_metadata


async def create_tag(user_id: str, raw_memo: Memo_raw_memo, lang: str="Korean") -> list[Memo_tag_name_and_id]:
    content: str=await _get_memo_content_and_metadata(raw_memo, lang)
    candidate_tags: list[Tag]=await extract_tags(content, user_id, lang)
    selected_tags: list[Tag]=await select_tags(content, candidate_tags, lang)
    assigned_tags: list[Memo_tag_name_and_id]=_assign_tags(selected_tags)
    
    return assigned_tags

async def _get_memo_content_and_metadata(raw_memo: Memo_raw_memo, lang: str) -> str: 
    return await process_metadata(raw_memo.content, raw_memo.image_urls, raw_memo.voice_urls, lang)
    
def _assign_tags(selected_tags: list[Tag]) -> list[Memo_tag_name_and_id]:
    return [
        Memo_tag_name_and_id(
            id=uuid.uuid4().hex if is_new_tag(selected_tag) else selected_tag.id,
            name=selected_tag.name,
            is_new=is_new_tag(selected_tag)
        ) for selected_tag in selected_tags
    ]

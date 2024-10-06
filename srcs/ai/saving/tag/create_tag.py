import asyncio
import uuid
from models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.saving.tag.utils import extract_tags, select_tags
from ai.saving._models import Tag
from ai.saving.utils import image_to_text, is_new_tag


async def create_tag(user_id: str, raw_memo: Memo_raw_memo, lang: str="Korean") -> list[Memo_tag_name_and_id]:
    raw_memo.content+='\n'+await _convert_image_to_content(raw_memo)
    candidate_tags: list[Tag]=await extract_tags(raw_memo.content, user_id, lang)
    selected_tags: list[Tag]=await select_tags(raw_memo.content, candidate_tags, lang)
    assigned_tags: list[Memo_tag_name_and_id]=_assign_tags(selected_tags)
    
    return assigned_tags

async def _convert_image_to_content(raw_memo: Memo_raw_memo) -> str:    
    image_to_text_tasks=[asyncio.to_thread(image_to_text, image) for image in raw_memo.image_urls]
    image_to_texts: list[str]=await asyncio.gather(*image_to_text_tasks)
    
    return "\n".join(image_to_texts)

def _assign_tags(selected_tags: list[Tag]) -> list[Memo_tag_name_and_id]:
    return [
        Memo_tag_name_and_id(
            id=uuid.uuid4().hex if is_new_tag(selected_tag) else selected_tag.id,
            name=selected_tag.name,
            is_new=is_new_tag(selected_tag)
        ) for selected_tag in selected_tags
    ]

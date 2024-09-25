import asyncio
from typing import Any, Coroutine
import uuid
from models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.saving.tag.utils import extract_tags, select_tags
from ai.saving._models import Tag
from ai.saving.utils.check_is_new_tag import is_new_tag


# TODO: NULL-378
async def create_tag(user_id: str, raw_memo: Memo_raw_memo, lang: str="Korean") -> list[Memo_tag_name_and_id]:
    candidate_tags=extract_tags(raw_memo.content, user_id, lang)
    selected_tags: list[Tag]=select_tags(raw_memo.content, candidate_tags, lang)
    assigned_tags: list[Memo_tag_name_and_id]=_assign_tags(selected_tags)
    
    return assigned_tags

def _assign_tags(selected_tags: list[Tag]) -> list[Memo_tag_name_and_id]:
    return [
        Memo_tag_name_and_id(
            id=uuid.uuid4().hex if is_new_tag(selected_tag) else selected_tag.id,
            name=selected_tag.name,
            is_new=is_new_tag(selected_tag)
        ) for selected_tag in selected_tags
    ]

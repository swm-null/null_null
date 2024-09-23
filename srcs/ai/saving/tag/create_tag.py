import asyncio
from typing import Any, Coroutine
import uuid
from models.memo_tags import Memos_raw_memo, Memos_tag
from ai.saving.tag.utils import extract_tags, select_tags
from ai.saving.tag.models import Tag


# TODO: NULL-378
async def create_tag(user_id: str, raw_memo: Memos_raw_memo, lang: str="Korean") -> list[Memos_tag]:
    candidate_tags=extract_tags(raw_memo.content, user_id, lang)
    selected_tags: list[Tag]=select_tags(raw_memo.content, candidate_tags, lang)
    assigned_tags: list[Memos_tag]=_assign_tags(selected_tags)
    
    return assigned_tags

def _assign_tags(selected_tags: list[Tag]) -> list[Memos_tag]:
    return [
        Memos_tag(
            name=selected_tag.name,
            is_new=False if selected_tag.name!=selected_tag.id else True,
            id=selected_tag.id if selected_tag.name!=selected_tag.id else uuid.uuid4().hex,
        ) for selected_tag in selected_tags
    ]

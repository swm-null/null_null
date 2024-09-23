import asyncio
from typing import Any, Coroutine
import uuid
from models.memo_tags import Memos_raw_memo, Memos_tag
from ai.saving.tag.utils import extract_tags, select_tags
from ai.saving.tag.models import Tag
from ai.utils import embedder


# TODO: NULL-378
async def create_tag(user_id: str, raw_memo: Memos_raw_memo, lang: str="Korean") -> list[Memos_tag]:
    candidate_tags=extract_tags(raw_memo.content, user_id, lang)
    selected_tags: list[Tag]=select_tags(raw_memo.content, candidate_tags, lang)
    embedded_and_assigned_tags: list[Memos_tag]=await _embed_and_assign_tags(selected_tags)
    
    return embedded_and_assigned_tags

async def _embed_and_assign_tags(selected_tags: list[Tag]) -> list[Memos_tag]:
    tasks: list[Coroutine[Any, Any, Memos_tag]]=[_embed_and_assign_tag(tag) for tag in selected_tags]
    processed_tags=await asyncio.gather(*tasks)
    
    return processed_tags

async def _embed_and_assign_tag(selected_tag: Tag) -> Memos_tag:
    embedding=await embedder.aembed_query(selected_tag.name)
    
    return Memos_tag(
            name=selected_tag.name,
            is_new=False if selected_tag.name!=selected_tag.id else True,
            id=selected_tag.id if selected_tag.name!=selected_tag.id else uuid.uuid4().hex,
            embedding=embedding
    )

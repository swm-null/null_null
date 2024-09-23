import asyncio
from models.memo_tags import Memos_raw_memo, Memos_tag
from ai.saving.tag.create_tag import create_tag


async def create_tags(user_id: str, raw_memos: list[Memos_raw_memo], lang: str="Korean") -> list[list[Memos_tag]]:
    return await asyncio.gather(*(create_tag(user_id, raw_memo, lang) for raw_memo in raw_memos))

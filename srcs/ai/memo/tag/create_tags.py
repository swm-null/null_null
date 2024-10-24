import asyncio
from routers._models.memo import Memo_raw_memo, Memo_tag_name_and_id
from ai.memo.tag.create_tag import create_tag


async def create_tags(user_id: str, raw_memos: list[Memo_raw_memo], lang: str="Korean") -> list[list[Memo_tag_name_and_id]]:
    return await asyncio.gather(*(create_tag(user_id, raw_memo, lang) for raw_memo in raw_memos))

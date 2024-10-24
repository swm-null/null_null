import asyncio
from ai.memo.structure._models.memo import Memo
from ai.memo.utils import process_metadata


async def extract_and_assign_metadata(memos: dict[int, Memo], lang: str) -> dict[int, Memo]:
    tasks={id: asyncio.create_task(_process_metadata_for_memo(memo, lang)) for id, memo in memos.items()}
    results = await asyncio.gather(*tasks.values())
    
    return {id: result for id, result in zip(tasks.keys(), results)}

async def _process_metadata_for_memo(memo: Memo, lang: str) -> Memo:    
    return Memo(
        content=memo.content,
        image_urls=memo.image_urls,
        metadata=await process_metadata(memo.content, memo.image_urls, lang),
        parent_tag_ids=memo.parent_tag_ids,
        timestamp=memo.timestamp
    )

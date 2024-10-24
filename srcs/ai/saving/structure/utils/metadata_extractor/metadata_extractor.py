import asyncio
from ai.saving._models.memo import Memo
from ai.saving.utils.metadata_extractor import process_metadata_for_memo


async def extract_and_assign_metadata(memos: dict[int, Memo], lang: str) -> dict[int, Memo]:
    tasks={id: asyncio.create_task(process_metadata_for_memo(memo, lang)) for id, memo in memos.items()}
    results = await asyncio.gather(*tasks.values())
    
    return {id: result for id, result in zip(tasks.keys(), results)}

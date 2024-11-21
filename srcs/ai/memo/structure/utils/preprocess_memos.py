import asyncio
from datetime import datetime
from routers._models.memo._models import Memo_memo_and_tags, Memo_processed_memo


async def preprocess_memos(memos_and_tags: list[Memo_memo_and_tags], lang: str) -> list[Memo_processed_memo]:
    tasks=[asyncio.create_task(_preprocess_memo(memo_and_tag, lang)) for memo_and_tag in memos_and_tags]
    
    return await asyncio.gather(*tasks)
    

async def _preprocess_memo(memo_and_tag: Memo_memo_and_tags, lang: str) -> Memo_processed_memo:
    # metadata_task=asyncio.create_task(process_metadata(memo_and_tag.content, memo_and_tag.image_urls, memo_and_tag.voice_urls, lang))
    
    return Memo_processed_memo(
        content=memo_and_tag.content,
        metadata=memo_and_tag.metadata,
        image_urls=memo_and_tag.image_urls,
        voice_urls=memo_and_tag.voice_urls,
        timestamp=memo_and_tag.timestamp if memo_and_tag.timestamp else datetime.now(),
        temporal_tags=memo_and_tag.tags,
        parent_tag_ids=[],
        embedding=[],
        embedding_metadata=[]
    )

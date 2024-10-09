import asyncio
from ai.saving.structure._models.memo import Memo
from ai.saving.utils import image_to_text, extract_metadata
from ai.saving.utils.chains.metadata_extractor_chain import Metadata_extractor_chain_output


async def extract_and_assign_metadata(memos: dict[int, Memo], lang: str) -> dict[int, Memo]:
    tasks=[_extract_and_assign_metadata(id, memo, lang) for id, memo in memos.items()]
    
    return dict(await asyncio.gather(*tasks))
        
async def _extract_and_assign_metadata(id: int, memo: Memo, lang: str) -> tuple[int, Memo]:
    extract_metadata_task = asyncio.to_thread(extract_metadata, memo.content, lang)
    image_to_text_tasks=[asyncio.to_thread(image_to_text, image) for image in memo.image_urls]
    
    extracted_metadata: list[Metadata_extractor_chain_output]=await asyncio.gather(extract_metadata_task)  # type: ignore
    image_to_texts: list[str]=await asyncio.gather(*image_to_text_tasks)
    
    return id, Memo(
        content=memo.content,
        image_urls=memo.image_urls,
        metadata=extracted_metadata[0].metadata + ''.join(f"\n{image_to_text}" for image_to_text in image_to_texts),
        parent_tag_ids=memo.parent_tag_ids,
        timestamp=memo.timestamp
    )

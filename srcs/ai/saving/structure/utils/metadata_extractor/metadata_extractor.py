import asyncio
from ai.saving.structure._models.memo import Memo
from ai.saving.utils import extract_metadata
from ai.saving.utils.link_extractor import extract_link
from ai.saving.utils.image_converter import convert_image_to_content
from ai.saving.utils.link_converter import convert_link_to_content


async def extract_and_assign_metadata(memos: dict[int, Memo], lang: str) -> dict[int, Memo]:
    tasks=[_extract_and_assign_metadata(id, memo, lang) for id, memo in memos.items()]
    
    return dict(await asyncio.gather(*tasks))
        
async def _extract_and_assign_metadata(id: int, memo: Memo, lang: str) -> tuple[int, Memo]:
    extracted_links: list[str]=extract_link(memo.content)
    
    tasks=[]
    if memo.content:
        tasks.append(asyncio.to_thread(extract_metadata, memo.content, lang))
    if memo.image_urls:
        tasks.append(convert_image_to_content(memo.image_urls, lang))
    if extracted_links:
        tasks.append(convert_link_to_content(extracted_links, lang))
    
    extracted_metadata: list[str]=await asyncio.gather(*tasks)
    print(extracted_metadata)
    
    return id, Memo(
        content=memo.content,
        image_urls=memo.image_urls,
        metadata="\n".join(extracted_metadata),
        parent_tag_ids=memo.parent_tag_ids,
        timestamp=memo.timestamp
    )

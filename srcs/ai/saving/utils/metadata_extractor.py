import asyncio
from ai.saving._models.memo import Memo
from ai.saving.utils.chains.metadata_extractor_chain import metadata_extractor_chain
from ai.saving.utils.image_converter import convert_image_to_content
from ai.saving.utils.link_converter import convert_link_to_content
from ai.saving.utils.link_extractor import extract_link


async def process_metadata_for_memo(memo: Memo, lang: str) -> Memo:    
    return Memo(
        content=memo.content,
        image_urls=memo.image_urls,
        metadata=await process_metadata(memo.content, memo.image_urls, lang),
        parent_tag_ids=memo.parent_tag_ids,
        timestamp=memo.timestamp
    )
    
async def process_metadata(content: str, image_urls: list[str], lang: str="Korean") -> str:
    extracted_links: list[str]=extract_link(content)
    
    tasks=[]
    if content:
        tasks.append(asyncio.create_task(_extract_metadata_from_content(content, lang)))
    if image_urls:
        tasks.append(asyncio.create_task(convert_image_to_content(image_urls, lang)))
    if extracted_links:
        tasks.append(asyncio.create_task(convert_link_to_content(extracted_links, lang)))
    
    extracted_metadata: list[str]=await asyncio.gather(*tasks)
    
    return "\n".join(extracted_metadata)

async def _extract_metadata_from_content(content: str, lang: str):
    return await metadata_extractor_chain.ainvoke({"content": content, "lang": lang})

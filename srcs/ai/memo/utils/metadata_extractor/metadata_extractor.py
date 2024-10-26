import asyncio
from ai.memo.utils.metadata_extractor.chains import metadata_extractor_chain
from ai.memo.utils.metadata_extractor.utils import image_to_text, link_to_text
from ai.memo.utils.link_extractor import extract_link


async def process_metadata(content: str, image_urls: list[str], lang: str="Korean") -> str:
    extracted_links: list[str]=extract_link(content)
    
    tasks=[]
    if content:
        tasks.append(asyncio.create_task(_extract_metadata_from_content(content, lang)))
    if image_urls:
        tasks.append(asyncio.create_task(image_to_text(image_urls, lang)))
    if extracted_links:
        tasks.append(asyncio.create_task(link_to_text(extracted_links, lang)))
    
    extracted_metadata: list[str]=await asyncio.gather(*tasks)
    
    return "\n".join(extracted_metadata)

async def _extract_metadata_from_content(content: str, lang: str):
    return await metadata_extractor_chain.ainvoke({"content": content, "lang": lang})

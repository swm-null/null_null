import asyncio
from typing import Any
from openai import BaseModel
from ai.memo.utils.metadata_extractor.chains import metadata_extractor
from ai.memo.utils.metadata_extractor.utils import image_to_text, link_to_text, record_to_text
from ai.memo.utils.link_extractor import extract_link


class _Metadata(BaseModel):
    metadata: list[Any]
    
async def process_metadata(content: str, image_urls: list[str], record_urls: list[str], lang: str="Korean") -> str:
    extracted_links: list[str]=extract_link(content)
    
    tasks=[]
    if content:
        tasks.append(asyncio.create_task(_extract_metadata_from_content(content, lang)))
    if image_urls:
        tasks.append(asyncio.create_task(image_to_text(image_urls, lang)))
    if record_urls:
        tasks.append(asyncio.create_task(record_to_text(record_urls, lang)))
    if extracted_links:
        tasks.append(asyncio.create_task(link_to_text(extracted_links, lang)))
    
    extracted_metadata=await asyncio.gather(*tasks)
    metadata=_Metadata(
        metadata=extracted_metadata
    ).model_dump_json()
    
    print(metadata)
    
    return metadata

async def _extract_metadata_from_content(content: str, lang: str):
    return await metadata_extractor(content, lang)
 
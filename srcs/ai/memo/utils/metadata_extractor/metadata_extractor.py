import asyncio
import logging
from openai import BaseModel
from ai.memo.utils.metadata_extractor.chains import metadata_extractor, Metadata_extractor_chain_output, Voice_record_summarizer_chain_output
from ai.memo.utils.metadata_extractor.utils import *
from ai.memo.utils.link_extractor import extract_link
from ai.memo.utils.text_summarizer.chains.text_summarizer_chain import Text_summarizer_chain_output


class _Metadata(BaseModel):
    content: str | None
    content_description: Metadata_extractor_chain_output | None=None
    image_descriptions: list[Image_description] | None=None
    voice_record_descriptions: list[Voice_record_summarizer_chain_output] | None=None
    link_descriptions: list[Text_summarizer_chain_output] | None=None
    
async def process_metadata(content: str, image_urls: list[str], voice_record_urls: list[str], lang: str="Korean") -> str:
    extracted_links: list[str]=extract_link(content)
    
    tasks=[]
    tasks_mapping={}

    if content:
        task=asyncio.create_task(_extract_metadata_from_content(content, lang))
        tasks.append(task)
        tasks_mapping[task]='content_description'
    if image_urls:
        task=asyncio.create_task(image_to_text(image_urls, lang))
        tasks.append(task)
        tasks_mapping[task]='image_descriptions'
    if voice_record_urls:
        task=asyncio.create_task(voice_record_to_text(voice_record_urls, lang))
        tasks.append(task)
        tasks_mapping[task]='voice_record_descriptions'
    if extracted_links:
        task=asyncio.create_task(link_to_text(extracted_links, lang))
        tasks.append(task)
        tasks_mapping[task]='link_descriptions'
    
    logging.info("process_metadata] tasks: " + str(tasks))
    completed_tasks=await asyncio.gather(*tasks)
    metadata_dict={
        tasks_mapping[task]: result
        for task, result in zip(tasks, completed_tasks)
    }
    metadata=_Metadata(content=content if content else None, **metadata_dict)
    logging.info("process_metadata] metadata: " + str(metadata))
    
    return metadata.model_dump_json(exclude_none=True)

async def _extract_metadata_from_content(content: str, lang: str):
    return await metadata_extractor(content, lang)
 
import asyncio
from pydantic import BaseModel
from ai.utils.link_content_fetcher import get_contents_from_link
from ai.memo.utils.text_summarizer.text_summarizer import summarize_text


class Link_descriptions(BaseModel):
    link_descriptions: list[str]
    
async def link_to_text(links: list[str], lang: str) -> Link_descriptions:
    link_contents: list[str]=await get_contents_from_link(links)
    summarize_text_tasks=[asyncio.create_task(summarize_text(content, lang)) for content in link_contents]
    link_to_texts: list[str]=await asyncio.gather(*summarize_text_tasks)
    
    return Link_descriptions(
        link_descriptions=link_to_texts
    )

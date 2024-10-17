import asyncio
from ai.saving.utils.link_content_fetcher import get_contents_from_link
from ai.saving.utils.text_summarizer import summarize_text


async def convert_link_to_content(links: list[str], lang: str) -> str:
    link_contents: list[str]=await get_contents_from_link(links)
    summarize_text_tasks=[asyncio.create_task(summarize_text(content, lang)) for content in link_contents]
    link_to_texts: list[str]=await asyncio.gather(*summarize_text_tasks)
    
    return "link description:\n"+"\n".join(link_to_texts)

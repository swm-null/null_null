import asyncio
from ai.utils.link_content_fetcher import get_contents_from_link
from ai.memo.utils.text_summarizer.text_summarizer import summarize_text


async def link_to_text(links: list[str], lang: str) -> str:
    link_contents: list[str]=await get_contents_from_link(links)
    summarize_text_tasks=[asyncio.create_task(summarize_text(content, lang)) for content in link_contents]
    link_to_texts: list[str]=await asyncio.gather(*summarize_text_tasks)
    
    return "link description:\n"+"\n".join(link_to_texts)

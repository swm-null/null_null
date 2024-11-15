import asyncio
from ai.memo.utils.text_summarizer.chains.text_summarizer_chain import Text_summarizer_chain_output
from ai.utils.link_content_fetcher import get_contents_from_link
from ai.memo.utils.text_summarizer.text_summarizer import summarize_text

    
async def link_to_text(links: list[str], lang: str) -> list[Text_summarizer_chain_output] | None:
    link_contents: list[str]=await get_contents_from_link(links)
    summarize_text_tasks=[asyncio.create_task(summarize_text(content, lang)) for content in link_contents]
    link_to_texts: list[Text_summarizer_chain_output]=await asyncio.gather(*summarize_text_tasks)
    
    return link_to_texts if link_to_texts else None

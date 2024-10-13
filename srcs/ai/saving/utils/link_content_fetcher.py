import asyncio
from typing import Optional
import aiohttp
import trafilatura


async def get_contents_from_link(links: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        fetch_tasks=[_fetch(session, link) for link in links]
        fetched_results=await asyncio.gather(*fetch_tasks)
    
    texts=[
        trafilatura.extract(fetched_result)
        for fetched_result in fetched_results if fetched_result
    ]
    
    return [text for text in texts if text]

async def _fetch(session, link: str) -> Optional[str]:
    async with session.get(link) as response:
        if response.status == 200:
            return await response.text()
        else:
            return None

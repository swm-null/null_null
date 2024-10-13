import asyncio
from typing import Optional
import aiohttp


async def get_contents_from_link(links: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        fetch_tasks=[_fetch(session, link) for link in links]
        fetched_results=await asyncio.gather(*fetch_tasks)
        
    return [result for result in fetched_results if result]

async def _fetch(session, link: str) -> Optional[str]:
    async with session.get(link) as response:
        if response.status == 200:
            return await response.text()
        else:
            return None

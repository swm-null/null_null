import asyncio
from typing import Optional
import aiohttp
import bs4
import trafilatura


async def get_contents_from_link(links: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        fetch_tasks=[_fetch(session, link) for link in links]
        fetched_results=await asyncio.gather(*fetch_tasks)
    
    texts=[
        "\n".join([
            _extract_og_data(fetched_result),
            trafilatura.extract(fetched_result) or ""
        ])
        for fetched_result in fetched_results if fetched_result
    ]
    
    return [text for text in texts if text]

async def _fetch(session: aiohttp.ClientSession, link: str) -> Optional[str]:
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    try:
        async with session.get(link, headers=headers, timeout=aiohttp.ClientTimeout(3)) as response:
            print(response)
            if response.status == 200:
                return await response.text()
            else:
                return None
    except:
        return None

def _extract_og_data(html: str) -> str:
    soup=bs4.BeautifulSoup(html, "html.parser")
    og_data={}
    
    # <meta property="og:title" content="Trafilatura">
    for meta in soup.find_all("meta"):
        property=meta.get("property")
        if property and property.startswith("og:"):
            og_data[property]=meta.get("content", "")
    
    return "\n".join([
        og_data.get("og:title", ""), 
        og_data.get("og:description", "")
    ])
    
    

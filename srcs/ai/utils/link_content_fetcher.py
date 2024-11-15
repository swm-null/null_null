import asyncio
import logging
from typing import Optional
import aiohttp
import bs4
import trafilatura


async def get_contents_from_link(links: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        fetch_tasks=[_fetch(session, link) for link in links]
        fetched_results: list[Optional[tuple[str, str]]]=await asyncio.gather(*fetch_tasks)
        filtered_results: list[tuple[str, str]] = list(filter(None, fetched_results))
    
    texts=[
        "\n".join([
            link,
            _extract_og_data(fetched_result),
            trafilatura.extract(fetched_result) or ""
        ])
        for link, fetched_result in filtered_results
    ]
    
    return [text for text in texts if text]

async def _fetch(session: aiohttp.ClientSession, link: str) -> Optional[tuple[str, str]]:
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-NL;q=0.8,en;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }
    try:
        async with session.get(link, headers=headers, timeout=aiohttp.ClientTimeout(3)) as response:
            logging.info("_fetch] %s\n", response)
            logging.info("_fetch] %s\n", response.content)
            if response.status == 200:
                return link, await response.text()
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
    
    

import asyncio
import pytest
from httpx import AsyncClient
from main import app
from models.memo.tags import Res_post_memo_tags


body={
    "user_id": "ccc55530-12ed-4a54-b420-025009c0509a",
    "raw_memos": [
        {
            "content": """
5GX 플래티넘(넷플릭스)
무제한
테더링/공유 120GB 집/이동전화 무제한, 영상/부가통화 300분 문자 기본 제공
T 우주 Netflix
넷플릭스 프리미엄 제공
T 멤버십
T 멤버십 VIP 혜택
스마트기기 이용요금
스마트기기 2회선 이용요금 무료
월 125,000원
선택약정 반영 시 93,705원

https://www.tworld.co.kr/web/product/callplan/NA00008719
https://asdf.com/this_is_invalid_link""",
            "images": [],
            "timestamp": "2024-10-05T16:21:27.136Z"
        }
    ]
}

@pytest.mark.asyncio
async def test_tags():
    tasks=[send_request_and_validate() for _ in range(3)]
    await asyncio.gather(*tasks)
    
UUID_LENGTH=32
async def send_request_and_validate():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response=await client.post("/memo/tags", json=body)
        
    res_model=Res_post_memo_tags.model_validate(response.json())
    
    assert response.status_code==200
    
    # tags
    assert len(res_model.tags)
    for tags in res_model.tags:
        for tag in tags:
            assert len(tag.id)==UUID_LENGTH

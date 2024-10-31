import asyncio
import textwrap
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from routers._models.embedding import Res_get_metadata_with_embedding


metadata_body={
    "content": textwrap.dedent("""
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
        https://asdf.com/this_is_invalid_link"""),
    "image_urls": [
        "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    ],
    "record_urls": [
        "https://sample-files-online.com/ko/samples/countdownload/17"
    ]
}

@pytest.mark.asyncio(loop_scope="session")
async def test_metadata():
    tasks=[send_request_and_validate() for _ in range(3)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/get-metadata-with-embedding", json=metadata_body)
        
    assert response.status_code==200
    res_model=Res_get_metadata_with_embedding.model_validate(response.json())
    validate_metadata(res_model)

    
def validate_metadata(res_model):
    assert "link_descriptions" in res_model.metadata
    assert "image_description" in res_model.metadata
    assert "record_transcription" in res_model.metadata
    

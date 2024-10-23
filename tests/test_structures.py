import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from models.memo.structures import Res_post_memo_structures


body_with_tag={
    "memos": [
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
            "image_urls": [
                "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
            ],
            "tags": [
                {
                    "id": "a70ab49dda364995ae34a1c76d52d8ef",
                    "name": "부가서비스",
                    "is_new": False
                },
                {
                    "id": "836f0c46a0664697b2d0a0cf1526f683",
                    "name": "이동통신 요금제",
                    "is_new": False
                },
                {
                    "id": "11111111111111111111111111111111",
                    "name": "이동통신 요금제", # should be ignored
                    "is_new": True
                },
                {
                    "id": "22222222222222222222222222222222",
                    "name": "이동통신요금제", # should be ignored
                    "is_new": True
                },
                {
                    "id": "ecedd0b9afc34f67aa2ede1029da1f41",
                    "name": "통신 요금제",
                    "is_new": False
                },
                {
                    "id": "33333333333333333333333333333333",
                    "name": "T 멤버십",
                    "is_new": False
                }
            ]
        }
    ],
    "user_id": "ccc55530-12ed-4a54-b420-025009c0509a"
}

body_without_tag={
    "memos": [
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
            "image_urls": [
                "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
            ],
            "tags": []
        }
    ],
    "user_id": "ccc55530-12ed-4a54-b420-025009c0509a"
}

@pytest.mark.asyncio(loop_scope="session")
async def test_structures_using_app():
    tasks=[asyncio.create_task(send_request_and_validate()) for _ in range(3)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
    # body with tag
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/memo/structures", json=body_with_tag)
        
    assert response.status_code==200
    res_model=Res_post_memo_structures.model_validate(response.json())
    validation_body_with_tag(res_model)
    
    # body without tag
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/memo/structures", json=body_without_tag)
        
    assert response.status_code==200
    res_model=Res_post_memo_structures.model_validate(response.json())
    validation_body_without_tag(res_model)

def validation_body_with_tag(res_model: Res_post_memo_structures):
    UUID_LENGTH=32
    
    # processed_memos
    for memo in res_model.processed_memos:
        assert "link description" in memo.metadata
        assert "image description" in memo.metadata    
        assert memo.parent_tag_ids   
        assert memo.metadata
        if memo.content:
            assert memo.embedding
    
    # structures
    for parent, childs in res_model.new_structure.items():
        assert len(parent)==UUID_LENGTH or len(parent)==UUID_LENGTH+4
        for child in childs:
            assert len(child)==UUID_LENGTH
        
    # new_tags
    for tag in res_model.new_tags:
        assert len(tag.id)==UUID_LENGTH
        assert tag.embedding
    assert [tag for tag in res_model.new_tags if tag.name=="T 멤버십"]
    
    # duplicated tags
    # assert not [tag for tag in res_model.new_tags if tag.name=="이동통신요금제" or tag.name=="이동통신 요금제"]
    
def validation_body_without_tag(res_model: Res_post_memo_structures):
    assert not [tag for tag in res_model.new_tags]

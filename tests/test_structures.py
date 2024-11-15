import asyncio
import textwrap
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from routers._models.memo.structures import Res_post_memo_structures


body_with_tag={
    "memos": [
        {
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
                https://asdf.com/this_is_invalid_link
            """),
            "image_urls": [],
            "voice_record_urls": [],
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
                    "id": "33333333333333333333333333333333",
                    "name": "T 멤버십",
                    "is_new": False
                }
            ],
            "metadata": '{"content":"\n5GX 플래티넘(넷플릭스)\n무제한\n테더링/공유 120GB 집/이동전화 무제한, 영상/부가통화 300분 문자 기본 제공\nT 우주 Netflix\n넷플릭스 프리미엄 제공\nT 멤버십\nT 멤버십 VIP 혜택\n스마트기기 이용요금\n스마트기기 2회선 이용요금 무료\n월 125,000원\n선택약정 반영 시 93,705원\n\nhttps://www.tworld.co.kr/web/product/callplan/NA00008719\nhttps://asdf.com/this_is_invalid_link","content_description":{"description":"이 메모는 5GX 플래티넘 요금제에 대한 정보로, 넷플릭스와 관련된 혜택 및 요금 세부사항을 포함하고 있습니다. 또한, T 멤버십 VIP 혜택과 스마트기기 이용요금에 대한 내용도 포함되어 있습니다.","keywords":["5GX 플래티넘","넷플릭스","무제한","테더링","T 멤버십","VIP 혜택","요금제","스마트기기"],"relative_time":{}},"image_descriptions":[{"simple_description":"구글 로고","image_description":"구글의 상징적인 로고가 다양한 색상으로 표현되어 있습니다.","ocr_text":""}],"voice_record_descriptions":[{"record_transcription":"이 영상은 유료 광고를 포함하고 있습니다. 오버워치 리그.","transcription_summary":"이 영상은 오버워치 리그에 대한 유료 광고를 포함하고 있습니다.","simple_description":"오버워치 리그 관련 유료 광고"}],"link_descriptions":[{"summary":"이 웹사이트는 T world의 다양한 서비스와 상품을 소개하는 페이지로, 특히 5GX 플래티넘 요금제와 넷플릭스 서비스에 대한 정보를 제공합니다. 사용자는 T world로 이동하여 T 우주, T roaming, T membership 등 다양한 서비스에 대한 이용 회선 정보를 확인할 수 있습니다. 이 페이지는 T world의 상품 및 서비스에 대한 접근을 용이하게 하며, 고객이 필요한 정보를 쉽게 찾을 수 있도록 구성되어 있습니다.","simple_description":"T world의 5GX 플래티넘 요금제 및 서비스 정보"}]}'
        }
    ],
    "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108"
}

body_without_content={
    "memos": [
        {
            "content": "",
            "image_urls": ["https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"],
            "voice_record_urls": [],
            "tags": [
                {
                    "id": "a70ab49dda364995ae34a1c76d52d8ef",
                    "name": "부가서비스",
                    "is_new": False
                }
            ],
            "metadata": '{"content":"\n5GX 플래티넘(넷플릭스)\n무제한\n테더링/공유 120GB 집/이동전화 무제한, 영상/부가통화 300분 문자 기본 제공\nT 우주 Netflix\n넷플릭스 프리미엄 제공\nT 멤버십\nT 멤버십 VIP 혜택\n스마트기기 이용요금\n스마트기기 2회선 이용요금 무료\n월 125,000원\n선택약정 반영 시 93,705원\n\nhttps://www.tworld.co.kr/web/product/callplan/NA00008719\nhttps://asdf.com/this_is_invalid_link","content_description":{"description":"이 메모는 5GX 플래티넘 요금제에 대한 정보로, 넷플릭스와 관련된 혜택 및 요금 세부사항을 포함하고 있습니다. 또한, T 멤버십 VIP 혜택과 스마트기기 이용요금에 대한 내용도 포함되어 있습니다.","keywords":["5GX 플래티넘","넷플릭스","무제한","테더링","T 멤버십","VIP 혜택","요금제","스마트기기"],"relative_time":{}},"image_descriptions":[{"simple_description":"구글 로고","image_description":"구글의 상징적인 로고가 다양한 색상으로 표현되어 있습니다.","ocr_text":""}],"voice_record_descriptions":[{"record_transcription":"이 영상은 유료 광고를 포함하고 있습니다. 오버워치 리그.","transcription_summary":"이 영상은 오버워치 리그에 대한 유료 광고를 포함하고 있습니다.","simple_description":"오버워치 리그 관련 유료 광고"}],"link_descriptions":[{"summary":"이 웹사이트는 T world의 다양한 서비스와 상품을 소개하는 페이지로, 특히 5GX 플래티넘 요금제와 넷플릭스 서비스에 대한 정보를 제공합니다. 사용자는 T world로 이동하여 T 우주, T roaming, T membership 등 다양한 서비스에 대한 이용 회선 정보를 확인할 수 있습니다. 이 페이지는 T world의 상품 및 서비스에 대한 접근을 용이하게 하며, 고객이 필요한 정보를 쉽게 찾을 수 있도록 구성되어 있습니다.","simple_description":"T world의 5GX 플래티넘 요금제 및 서비스 정보"}]}'
        }
    ],
    "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108"
}

@pytest.mark.asyncio(loop_scope="session")
async def test_structures_using_app():
    tasks=[asyncio.create_task(send_request_and_validate()) for _ in range(2)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
    # body with tag
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/memo/structures", json=body_with_tag)
        
    assert response.status_code==200
    res_model=Res_post_memo_structures.model_validate(response.json())
    validation_body_with_tag(res_model)

    # body without content
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/memo/structures", json=body_without_content)
        
    assert response.status_code==200
    res_model=Res_post_memo_structures.model_validate(response.json())
    validation_body_without_content(res_model)
    
def validation_body_with_tag(res_model: Res_post_memo_structures):
    UUID_LENGTH=32
    
    # processed_memos
    for memo in res_model.processed_memos:
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
    assert [tag for tag in res_model.new_tags if tag.name=="T 멤버십"]
    
def validation_body_without_content(res_model: Res_post_memo_structures):  
    # processed_memos
    for memo in res_model.processed_memos:
        assert memo.parent_tag_ids   
        assert not memo.content
        assert not memo.embedding
        assert memo.metadata
        assert memo.embedding_metadata

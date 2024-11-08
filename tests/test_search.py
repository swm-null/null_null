import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from routers._models.search import Res_post_search_ai
from routers._models.search import Res_post_search_db


similarity_body={
    "query": "요금제 관련 정보 좀 찾아줘",
    "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108"
}

regex_body={
    "query": "주민등록번호 좀 찾아줘",
    "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108"
}

db_body={
    "query": "주민등록번호 좀 찾아줘",
    "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108"
}

@pytest.mark.asyncio(loop_scope="session")
async def test_search():
    tasks=[send_request_and_validate() for _ in range(3)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
    # similar search with ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/search/ai", json=similarity_body)
        
    assert response.status_code==200
    res_model=Res_post_search_ai.model_validate(response.json())
    validation_similarity(res_model)
    
    # regex search with ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/search/ai", json=regex_body)
        
    assert response.status_code==200
    res_model=Res_post_search_ai.model_validate(response.json())
    validation_regex(res_model)
    
    # search with db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/search/db", json=db_body)
        assert response.status_code==200
    res_model=Res_post_search_db.model_validate(response.json())
    
def validation_similarity(res_model):
    pass
    
def validation_regex(res_model):
    pass
    
def validation_db(res_model):
    pass

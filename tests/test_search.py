import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from models.search import Res_post_search


body={
    "content": "요금제 관련 정보 좀 찾아줘",
    "user_id": "ccc55530-12ed-4a54-b420-025009c0509a"
}

@pytest.mark.asyncio(loop_scope="session")
async def test_search():
    tasks=[send_request_and_validate() for _ in range(3)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/search", json=body)
        
    assert response.status_code==200
    res_model=Res_post_search.model_validate(response.json())
    validation(res_model)
    
def validation(res_model):
    pass
    

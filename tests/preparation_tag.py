import asyncio
import textwrap
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from routers._models.memo.tags import Res_post_memo_tags


basebody={
  "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108",
  "raw_memos": [
    {
      "content": "",
      "image_urls": [],
      "voice_urls": [],
      "timestamp": "2024-11-07T04:32:29.216Z"
    }
  ]
}


@pytest.mark.asyncio(loop_scope="session")
async def test_tags():
    tasks=[asyncio.create_task(send_request_and_validate()) for _ in range(1)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
  global contents
  for content in contents:
    json_body=basebody
    json_body["raw_memos"][0]["content"]=content
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response=await client.post("/memo/tags", json=json_body)
        
    assert response.status_code==200
    

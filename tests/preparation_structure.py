import asyncio
import json
import struct
import textwrap
import pytest
from httpx import ASGITransport, AsyncClient
from ai.memo import structure
from main import app
from routers._models.memo.tags import Res_post_memo_tags


tag_basebody={
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

structure_basebody={
  "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108",
  "memos": [
    {
      "content": "",
      "image_urls": [],
      "voice_urls": [],
      "timestamp": "2024-11-07T16:25:30.643Z",
      "tags": []
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
    tag_body=tag_basebody
    tag_body["raw_memos"][0]["content"]=content
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        res_tags=await client.post("/memo/tags", json=tag_body)
        
    assert res_tags.status_code==200
    res_model: Res_post_memo_tags=Res_post_memo_tags.model_validate(res_tags.json())
    
    ###
    
    structure_body=structure_basebody
    structure_body["memos"][0]["content"]=content
    structure_body["memos"][0]["tags"]=[{"id": tag.id, "name": tag.name, "is_new": tag.is_new} for tag in res_model.tags[0]]
    
    print(structure_body)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        res_structures=await client.post("/memo/structures", json=structure_body)
    
    assert res_structures.status_code==200

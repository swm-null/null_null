from fastapi import APIRouter
from ai.memo.structure import get_new_structures
from ai.memo.tag import create_tag, create_tags
from routers._models import *


router=APIRouter(tags=["memo"])

@router.post("/memo/tags", response_model=Res_post_memo_tags)
async def post_memo_tags(body: Body_post_memo_tags):
    tags_and_metadatas=await create_tags(body.user_id, body.raw_memos)
    return Res_post_memo_tags(
        tags_and_metadata=[
            Res_post_memo_tag(
                tags=tags,
                metadata=metadata
        ) for tags, metadata in tags_and_metadatas
    ])

@router.post("/memo/tag", response_model=Res_post_memo_tag)
async def post_memo_tag(body: Body_post_memo_tag):
    tags, metadata=await create_tag(body.user_id, body.raw_memo)
    return Res_post_memo_tag(tags=tags, metadata=metadata)

@router.post("/memo/structures", response_model=Res_post_memo_structures)
async def post_memo_structures(body: Body_post_memo_structures):
    return await get_new_structures(body.user_id, body.memos)

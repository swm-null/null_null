from fastapi import APIRouter
from routers._models.memo import *


router=APIRouter(tags=["memo"])

@router.post("/memo/tags", response_model=Res_post_memo_tags)
async def post_memo_tags(body: Body_post_memo_tags):
    return Res_post_memo_tags(tags=await create_tags(body.user_id, body.raw_memos))

@router.post("/memo/tag", response_model=Res_post_memo_tag)
async def post_memo_tag(body: Body_post_memo_tag):
    return Res_post_memo_tag(tags=await create_tag(body.user_id, body.raw_memo))

@router.post("/memo/structures", response_model=Res_post_memo_structures)
async def post_memo_structures(body: Body_post_memo_structures):
    processed_memos, relations, tags=await process_memos(body.user_id, body.memos)
    structure, reversed_structure=await get_structure(body.user_id, relations)
    
    return Res_post_memo_structures(
        processed_memos=processed_memos,
        new_tags=tags,
        new_structure=structure,
        new_reversed_structure=reversed_structure
    )

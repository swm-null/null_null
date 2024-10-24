from fastapi import APIRouter
from routers._models.search import *
from ai.search import search_memo


router=APIRouter(tags=["search"])

@router.post("/search", response_model=Res_post_search)
async def post_search(body: Arg_post_search):
    return await search_memo(body.content, body.user_id)

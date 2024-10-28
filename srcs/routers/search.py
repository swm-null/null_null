from fastapi import APIRouter
from routers._models.search import *
from ai.search import search_memo


router=APIRouter(tags=["search"])

@router.post("/search/ai", response_model=Res_post_search_ai)
async def post_search_ai(body: Arg_post_search_ai):
    return await search_memo_using_ai(body.content, body.user_id)

@router.post("/search/db")
def post_search_db(body: Arg_post_search_db):
    return search_memo_using_db(body.content, body.user_id)

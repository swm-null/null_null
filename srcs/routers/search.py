from fastapi import APIRouter
from ai.search import search_memo_using_db, search_memo_using_ai
from routers._models.search import *


router=APIRouter(tags=["search"])

@router.post("/search/ai", response_model=Res_post_search_ai)
async def post_search_ai(body: Arg_post_search_ai):
    return await search_memo_using_ai(body.content, body.user_id)

@router.post("/search/db", response_model=Res_post_search_db)
def post_search_db(body: Arg_post_search_db):
    return search_memo_using_db(body.content, body.user_id)

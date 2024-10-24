from datetime import datetime
from fastapi import APIRouter
from routers._models import *
from routers.memo import post_memo_structures


router=APIRouter(tags=["parser"])

@router.post("/kakao-parser", response_model=Res_post_memo_structures)
async def post_kakao_parser(body: Body_post_kakao_parser):
    parsed_contents: list[tuple[str, datetime]]=await kakao_parser(content=body.content, type=body.type)
    raw_memos: list[Memo_raw_memo]=[
        Memo_raw_memo(content=content, timestamp=timestamp)
        for content, timestamp in parsed_contents
    ]
    tag_results: list[list[Memo_tag_name_and_id]]=Res_post_memo_tags(tags=await create_tags(body.user_id, raw_memos)).tags
    
    return post_memo_structures(
        Body_post_memo_structures(
            user_id=body.user_id,
            memos=[
                Memo_memo_and_tags(
                    content=memo.content,
                    timestamp=memo.timestamp,
                    tags=tags
                )
                for memo, tags in zip(raw_memos, tag_results)
            ]
        )
    )

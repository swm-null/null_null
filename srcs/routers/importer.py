from datetime import datetime
from fastapi import APIRouter
from ai.memo.tag import create_tags
from ai.parser import kakao_parser
from routers._models import *
from routers.memo import post_memo_structures, post_memo_tags


router=APIRouter(tags=["importer"])

@router.post("/kakao-parser", response_model=Res_post_memo_structures)
async def post_kakao_parser(body: Body_post_kakao_parser):
    parsed_contents: list[tuple[str, datetime]]=await kakao_parser(content=body.content, type=body.type)
    raw_memos: list[Memo_raw_memo]=[
        Memo_raw_memo(content=content, timestamp=timestamp)
        for content, timestamp in parsed_contents
    ]
    tag_results: Res_post_memo_tags=await post_memo_tags(
        Body_post_memo_tags(
            user_id=body.user_id,
            raw_memos=raw_memos
        )
    )
    
    return await post_memo_structures(
        Body_post_memo_structures(
            user_id=body.user_id,
            memos=[
                Memo_memo_and_tags(
                    content=memo.content,
                    timestamp=memo.timestamp,
                    metadata=tags.metadata,
                    tags=tags.tags
                )
                for memo, tags in zip(raw_memos, tag_results.tags_and_metadata)
            ]
        )
    )

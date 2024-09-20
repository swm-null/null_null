import asyncio
from fastapi import FastAPI, status
import uvicorn
import logging

from init import init
from ai.utils import embedder
from ai.searching import search
from ai.saving import single_processor, batch_processor, memo_structurer, memos_structurer
from ai.saving.parser import kakao_parser
from models import *

from ai.searching_deprecated.regex_generator import get_regex
from ai.searching_deprecated.query_analyzer import Query_Type, query_analyzer
from ai.searching_deprecated.similarity_search import similarity_search
from ai.searching_deprecated.tag_finder import find_tag_ids


app = FastAPI(
    title="Oatnote AI",
    description="after PR #61, https://github.com/swm-null/null_null/pull/61",
    version="0.2.6",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search", response_model=Res_post_search)
def post_search(body: Arg_post_search):
    return search(body.content, body.user_id)

@app.post("/memos", response_model=Res_post_memos, status_code=status.HTTP_200_OK)
def post_memos(body: Arg_post_memos):
    processed_memos=asyncio.run(batch_processor(body.memos, body.user_id))
    
    return Res_post_memos(
        processed_memos=processed_memos,
        new_structure=memos_structurer(processed_memos, body.user_id)
    )

@app.post("/memo", response_model=Res_post_memo, status_code=status.HTTP_200_OK)
def post_memo(body: Arg_post_memo):
    processed_memo=single_processor(body.memo, body.user_id)
    
    return Res_post_memo(
        processed_memo=processed_memo,
        new_structure=memo_structurer(processed_memo, body.user_id)
    )
    
@app.post("/get-embedding", response_model=Res_get_embedding)
def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(
        embedding=embedder.embed_query(body.content)
    )

@app.post("/kakao-parser", response_model=Res_post_memos)
def post_kakao_parser(body: Arg_kakao_parser):
    parsed_memos: list[tuple[str, datetime]]=kakao_parser(body.content, body.type)
    memos: list[Memos_raw_memo]=[
        Memos_raw_memo(
            content=content, 
            timestamp=timestamp
        ) for content, timestamp in parsed_memos
    ]
    
    return post_memos(Arg_post_memos(
        user_id=body.user_id,
        memos=memos
    ))

if __name__ == '__main__':
    uvicorn.run(app)

@app.post("/search_deprecated", response_model=Res_search, deprecated=True)
def search_depreacted(body: Arg_search):
    return_content: Res_search=Res_search()

    return_content.type=query_analyzer(body.content)

    if return_content.type == Query_Type.unspecified:
        logging.info("[/search] unspecified query: %s", body.content)
        return_content.type=Query_Type.similarity

    if return_content.type == Query_Type.regex:
        return_content.regex=get_regex(body.content)

    elif return_content.type == Query_Type.tags:
        return_content.tags=find_tag_ids(body.content)
        # if the tag search result is None
        if return_content.tags == None:
            # then trying similarity search
            return_content.type=Query_Type.similarity
        
    if return_content.type == Query_Type.similarity:
        return_content.processed_message, return_content.ids=similarity_search(body.content)

    logging.info("[/search] query: %s / query type: %s \nreturn: %s", body.content, return_content.type, return_content)

    return return_content

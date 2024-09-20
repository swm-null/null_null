import asyncio
from fastapi import FastAPI, status
import uvicorn
import logging
from init import init

from ai.utils.embedder import embedder
from ai.saving.processor.single_processor import single_processor, single_adder_deprecated
from ai.saving.processor.batch_processor import batch_processor
from ai.saving.structurer.structurer import memo_structurer, memos_structurer

from ai.searching_deprecated.regex_generator import get_regex
from ai.searching_deprecated.query_analyzer import Query_Type, query_analyzer
from ai.searching_deprecated.similarity_search import similarity_search
from ai.searching_deprecated.tag_finder import find_tag_ids

from ai.saving.parser import kakao_parser as kp

from models.add_memo import *
from models.memos import *
from models.memo import *
from models.search import *
from models.search_deprecated import *
from models.get_embedding import *
from models.kakao_parser import *
from ai.searching.search import search


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
    
@app.post("/get_embedding/", response_model=Res_get_embedding)
def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(
        embedding=embedder.embed_query(body.content)
    )

@app.post("/kakao-parser/", response_model=Res_post_memos)
def kakao_parser(body: Arg_kakao_parser):
    parsed_memos: list[tuple[str, datetime]]=kp.kakao_parser(body.content, body.type)
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

@app.post("/add_memo/", deprecated=True, response_model=Res_add_memo, status_code=status.HTTP_200_OK)
def add_memo(body: Arg_add_memo):
    return single_adder_deprecated(body)

if __name__ == '__main__':
    uvicorn.run(app)

@app.post("/test_format_directories")
async def test_format_directories():
    from ai.saving.tag.locator.get_formatted_directories import get_formatted_directories
    print(get_formatted_directories("test2"))
    return get_formatted_directories("test2")

@app.post("/clear_tags")
async def clear_tags():
    from ai.database.collections.tag_store import tag_collection
    tag_collection.delete_many({"uId": "test2"})
    
@app.post("/clear_edges")
async def clear_edges():
    from ai.database.collections.tag_edges import tag_edges_collection
    tag_edges_collection.delete_many({"uId": "test2"})
    
@app.post("/create_dummy")
async def create_dummy():

    from ai.database.collections.tag_edges import tag_edges_collection
    tag_edges_collection.delete_many({"uId": "test2"})
    tag_edges_collection.insert_one({
        "uId": "test2",
        "edges": {
            "@test@": ["!음식", "!여행", "!라면"],
            "!음식": ["!라면", "!떡볶이", "!고추장"],
            "!여행": ["!프랑스", "!네덜란드"],
            "!라면": ["!떡라면", "!날치알라면"],
        }
    })

    # 이거 임베딩 동기라 느리네 아이고..
    from ai.database.collections.tag_store import tag_collection
    tag_collection.delete_many({"uId": "test2"})
    tag_collection.insert_many([
        {
            "uId": "test2",
            "name": "@",
            "_id": "@test@",
            "embedding": embedder.embed_query("@"),
        },
        {
            "uId": "test2",
            "name": "음식",
            "_id": "!음식",
            "embedding": embedder.embed_query("음식"),
        },
        {
            "uId": "test2",
            "name": "라면",
            "_id": "!라면",
            "embedding": embedder.embed_query("라면"),
        },
        {
            "uId": "test2",
            "name": "떡볶이",
            "_id": "!떡볶이",
            "embedding": embedder.embed_query("떡볶이"),
        },
        {
            "uId": "test2",
            "name": "고추장",
            "_id": "!고추장",
            "embedding": embedder.embed_query("고추장"),
        },
        {
            "uId": "test2",
            "name": "여행",
            "_id": "!여행",
            "embedding": embedder.embed_query("여행"),
        },
        {
            "uId": "test2",
            "name": "프랑스",
            "_id": "!프랑스",
            "embedding": embedder.embed_query("프랑스"),
        },
        {
            "uId": "test2",
            "name": "네덜란드",
            "_id": "!네덜란드",
            "embedding": embedder.embed_query("네덜란드"),
        },
        {
            "uId": "test2",
            "name": "떡라면",
            "_id": "!떡라면",
            "embedding": embedder.embed_query("떡라면"),
        },
        {
            "uId": "test2",
            "name": "날치알라면",
            "_id": "!날치알라면",
            "embedding": embedder.embed_query("날치알라면"),
        },
    ])

@app.post("/search_deprecated/", response_model=Res_search, deprecated=True)
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

import asyncio
from fastapi import FastAPI, status
import uvicorn
import logging

from init import init
from ai.utils import embedder
from ai.searching import search
from ai.saving.tag import create_tag, create_tags
from ai.saving.structure import process_memos, get_structure
from models import *

app = FastAPI(
    title="Oatnote AI",
    description="after PR #62, https://github.com/swm-null/null_null/pull/62",
    version="0.2.7",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search", response_model=Res_post_search)
def post_search(body: Arg_post_search):
    return search(body.content, body.user_id)
    
@app.post("/get-embedding", response_model=Res_get_embedding)
def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(
        embedding=embedder.embed_query(body.content)
    )

@app.post("/memo/tags", response_model=Res_post_memo_tags)
def post_memo_tags(body: Body_post_memo_tags):
    return Res_post_memo_tags(tags=asyncio.run(create_tags(body.user_id, body.raw_memos)))

@app.post("/memo/tag", response_model=Res_post_memo_tag)
def post_memo_tag(body: Body_post_memo_tag):
    return Res_post_memo_tag(tags=asyncio.run(create_tag(body.user_id, body.raw_memo)))
    
@app.post("/memo/structures", response_model=Res_post_memo_structures)
def post_memo_structures(body: Body_post_memo_structures):
    processed_memos, relations, tags=asyncio.run(process_memos(body.user_id, body.memos))
    structure: dict[str, list[str]]=get_structure(body.user_id, relations)

    return Res_post_memo_structures(
        processed_memos=processed_memos,
        tags_relations=Memo_relations(added=relations, deleted=[]),
        new_tags=tags,
        new_structure=structure
    )
    

if __name__ == '__main__':
    uvicorn.run(app)

# deprecated imports
from ai.searching_deprecated.regex_generator import get_regex
from ai.searching_deprecated.query_analyzer import Query_Type, query_analyzer
from ai.searching_deprecated.similarity_search import similarity_search
from ai.searching_deprecated.tag_finder import find_tag_ids
from ai.saving import single_processor, batch_processor
from ai.saving.structurer_deprecated.structurer import memo_structurer, memos_structurer
from ai.saving.parser import kakao_parser
from models.memos_deprecated import *
from models.memo_deprecated import *
from models.search_deprecated import *
from models.kakao_parser import *

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

@app.post("/memos", response_model=Res_post_memos, status_code=status.HTTP_200_OK, deprecated=True)
def post_memos(body: Arg_post_memos):
    processed_memos=asyncio.run(batch_processor(body.memos, body.user_id))
    
    return Res_post_memos(
        processed_memos=processed_memos,
        new_structure=memos_structurer(processed_memos, body.user_id)
    )

@app.post("/memo", response_model=Res_post_memo, status_code=status.HTTP_200_OK, deprecated=True)
def post_memo(body: Arg_post_memo):
    processed_memo=single_processor(body.memo, body.user_id)
    
    return Res_post_memo(
        processed_memo=processed_memo,
        new_structure=memo_structurer(processed_memo, body.user_id)
    )
    
@app.post("/kakao-parser", response_model=Res_post_memos, deprecated=True)
def post_kakao_parser(body: Arg_kakao_parser):
    parsed_memos: list[tuple[str, datetime]]=kakao_parser(body.content, body.type)
    memos: list[Memo_raw_memo]=[
        Memo_raw_memo(
            content=content, 
            timestamp=timestamp
        ) for content, timestamp in parsed_memos
    ]
    
    return post_memos(Arg_post_memos(
        user_id=body.user_id,
        memos=memos
    ))

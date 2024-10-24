from fastapi import FastAPI
import uvicorn

from init import init
from models import *
from ai.utils import embedder
from ai.searching import search_memo
from ai.saving.tag import create_tag, create_tags
from ai.saving.structure import process_memos, get_structure
from ai.saving.utils import process_metadata
from ai.saving.parser import kakao_parser


app = FastAPI(
    title="Oatnote AI",
    description="after PR #91, https://github.com/swm-null/null_null/pull/91",
    version="0.2.41",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search", response_model=Res_post_search)
async def post_search(body: Arg_post_search):
    return await search_memo(body.content, body.user_id)

@app.post("/get-embedding", response_model=Res_get_embedding)
def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(embedding=embedder.embed_query(body.content))

@app.post("/get-metadata-with-embedding", response_model=Res_get_metadata_with_embedding)
async def post_get_metadata_with_embedding(body: Body_get_metadata_with_embedding):
    metadata=await process_metadata(body.content, body.image_urls)
    
    return Res_get_metadata_with_embedding(
        metadata=metadata,
        embedding_metadata=await embedder.aembed_query(metadata)
    )

@app.post("/memo/tags", response_model=Res_post_memo_tags)
async def post_memo_tags(body: Body_post_memo_tags):
    return Res_post_memo_tags(tags=await create_tags(body.user_id, body.raw_memos))

@app.post("/memo/tag", response_model=Res_post_memo_tag)
async def post_memo_tag(body: Body_post_memo_tag):
    return Res_post_memo_tag(tags=await create_tag(body.user_id, body.raw_memo))

@app.post("/memo/structures", response_model=Res_post_memo_structures)
async def post_memo_structures(body: Body_post_memo_structures):
    processed_memos, relations, tags=await process_memos(body.user_id, body.memos)
    structure, reversed_structure=await get_structure(body.user_id, relations)
    
    return Res_post_memo_structures(
        processed_memos=processed_memos,
        new_tags=tags,
        new_structure=structure,
        new_reversed_structure=reversed_structure
    )

@app.post("/kakao-parser", response_model=Res_post_memo_structures)
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

if __name__ == '__main__':
    uvicorn.run(app)

# deprecated
from ai.saving.utils.metadata_extractor import _extract_metadata_from_content
@app.post("/get-metadata", response_model=Res_get_metadata, deprecated=True)
async def post_get_metadata(body: Body_get_metadata):
    return await _extract_metadata_from_content(body.content, "Korean")

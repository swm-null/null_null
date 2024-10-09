import asyncio
from fastapi import FastAPI
import uvicorn

from init import init
from models import *
from ai.utils import embedder
from ai.searching import search_memo
from ai.saving.tag import create_tag, create_tags
from ai.saving.structure import process_memos, get_structure
from ai.saving.utils import extract_metadata

app = FastAPI(
    title="Oatnote AI",
    description="after PR #73, https://github.com/swm-null/null_null/pull/73",
    version="0.2.22",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search", response_model=Res_post_search)
def post_search(body: Arg_post_search):
    return search_memo(body.content, body.user_id)

@app.post("/get-embedding", response_model=Res_get_embedding)
def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(embedding=embedder.embed_query(body.content))

@app.post("/get-metadata", response_model=Res_get_metadata)
def post_get_metadata(body: Body_get_metadata):
    return extract_metadata(body.content)

@app.post("/get-metadata-with-embedding", response_model=Res_get_metadata_with_embedding)
def post_get_meta_data_with_embedding(body: Body_get_metadata_with_embedding):
    metadata=extract_metadata(body.content).metadata
    
    return Res_get_metadata_with_embedding(
        metadata=metadata,
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

    validate_ids(relations, tags)
    
    return Res_post_memo_structures(
        processed_memos=processed_memos,
        tags_relations=Memo_relations(added=relations, deleted=[]),
        new_tags=tags,
        new_structure=structure
    )

def validate_ids(relations: list[Memo_tag_relation], tags: list[Memo_tag]):
    from fastapi import HTTPException
    for relation in relations:
        if (len(relation.child_id) != 32 and len(relation.child_id) != 36) or (len(relation.parent_id) != 32 and len(relation.parent_id) != 36):
            raise HTTPException(500)
    for tag in tags:
        if len(tag.id) != 32:
            raise HTTPException(500)

if __name__ == '__main__':
    uvicorn.run(app)

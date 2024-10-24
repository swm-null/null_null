from fastapi import APIRouter
from ai.memo.utils import process_metadata
from routers._models import *
from ai.utils import embedder


router=APIRouter(tags=["embedding"])

@router.post("/get-embedding", response_model=Res_get_embedding)
def get_embedding(body: Body_get_embedding):
    return Res_get_embedding(embedding=embedder.embed_query(body.content))

@router.post("/get-metadata-with-embedding", response_model=Res_get_metadata_with_embedding)
async def post_get_metadata_with_embedding(body: Body_get_metadata_with_embedding):
    metadata=await process_metadata(body.content, body.image_urls)
    
    return Res_get_metadata_with_embedding(
        metadata=metadata,
        embedding_metadata=await embedder.aembed_query(metadata)
    )

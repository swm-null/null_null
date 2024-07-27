# from database import connection
from typing import Optional
from fastapi import FastAPI, status
from ai.for_search import query_analyzer as qa
from ai.for_search import regex_generator as rg
from ai.for_search import tag_finder as tf
from ai.for_search import similarity_search as ss
from ai.for_save import query_extractor as qe
import traceback
import uvicorn, uvicorn.logging
import logging
from logger import *
from models.add_memo import *
from models.search import *
from models.get_embedding import *
from init import init

app = FastAPI()
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

@app.post("/search/", response_model=Res_search)
async def search(body: Arg_search):
    return_content: Res_search=Res_search()

    return_content.type=qa.query_analyzer(body.content)

    if return_content.type == qa.Query_Type.regex:
        return_content.regex=rg.get_regex(body.content)

    elif return_content.type == qa.Query_Type.tags:
        return_content.tags=tf.find_tag_ids(body.content)
        # if the tag search result is None
        if return_content.tags == None:
            # then trying similarity search
            return_content.type = qa.Query_Type.similarity
        
    if return_content.type == qa.Query_Type.similarity:
        return_content.processed_message, return_content.ids=ss.similarity_search(body.content)

    logging.info("[/search] query: %s / query type: %s \nreturn: %s", body.content, return_content.type, return_content)

    return return_content

@app.post("/add_memo/", response_model=Res_add_memo, status_code=status.HTTP_200_OK)
async def add_memo(body: Arg_add_memo):
    existing_tag_ids: list[str]
    new_tags: list[Res_memo_tag]
    existing_tag_ids, new_tags = qe.query_extractor(body.content)

    return Res_add_memo(
        memo_embeddings=qe.embeddings.embed_query(body.content),
        existing_tag_ids=existing_tag_ids,
        new_tags=new_tags
    )

@app.post("/get_embedding/", response_model=Res_get_embedding)
async def get_embedding(body: Arg_get_embedding):
    return Res_get_embedding(
        embedding=qe.embeddings.embed_query(body.content)
    )

if __name__ == '__main__':
    uvicorn.run(app)

# from database import connection
from typing import Optional, Literal
from fastapi import FastAPI, status
from pydantic import BaseModel
from ai.for_search import query_analyzer as qa
from ai.for_search import regex_generator as rg
from ai.for_search import tag_finder as tf
from ai.for_search import similarity_search as ss
from ai.for_save import query_extractor as qe
import traceback
import uvicorn, uvicorn.logging
import database.collections
from langchain_core.documents.base import Document
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from logger import sentry_init
import logging

app = FastAPI()
app.add_middleware(SentryAsgiMiddleware)
    
@app.get("/")
async def default():
    return "yes. it works."

class Arg_search(BaseModel):
    query: str

class Res_search(BaseModel):
    type: qa.Query_Type=qa.Query_Type.unspecified
    processed_message: Optional[str]=None
    ids: Optional[list[str]]=None
    regex: Optional[str]=None
    tags: Optional[list[str]]=None

@app.post("/search/", response_model=Res_search)
async def search(body: Arg_search):
    return_content: Res_search=Res_search()

    try:
        return_content.type=qa.query_analyzer(body.query)

        if return_content.type == qa.Query_Type.regex:
            return_content.regex=rg.get_regex(body.query)
    
        elif return_content.type == qa.Query_Type.tags:
            return_content.tags=tf.find_tag_ids(body.query)
            # if the tag search result is None
            if return_content.tags == None:
                # then trying similarity search
                return_content.type = qa.Query_Type.similarity
            
        if return_content.type == qa.Query_Type.similarity:
            return_content.processed_message, return_content.ids=ss.similarity_search(body.query)
    except:
        logging.error("[/search] %s", traceback.format_exc())
        return_content.type=qa.Query_Type.unspecified

    logging.info("[/search] query: %s / query type: %s \nreturn: %s", body.query, return_content.type, return_content)

    return return_content

# ------------ deprecated
class Res_get_user_query(BaseModel):
    type: int
    content: list[str]

@app.get("/user_query/", response_model=Res_get_user_query, deprecated=True)
async def get_user_query(query: str):
    query_type=qa.query_analyzer(query)

    return_content: Optional[list[str]]=None

    try:
        if query_type == qa.Query_Type.regex:
            query_type=2
            return_content=[rg.get_regex(query)]
            
        elif query_type == qa.Query_Type.tags:
            query_type=3
            return_content=tf.find_tag_name(query)

        if query_type == qa.Query_Type.similarity or return_content==None:
            query_type=1
            return_content=ss.search_similar_memos(query)
    except:
        logging.error("[/user_query] %s", traceback.format_exc())
        query_type=0

    logging.info("[/user_query] user query: %s / query type: %s \nreturn: %s", query, query_type, return_content)

    return {
        "type": query_type,
        "content": return_content
    }

@app.get("/user_query_with_processed/", response_model=Res_get_user_query, deprecated=True)
async def get_user_query_with_processed(query: str):
    response=await get_user_query(query)

    if response["type"]==1: # similarity search
        processed_result: str=ss.process_result(query, response["content"])
        logging.info("processed result: %s", processed_result)
        
        return {
            "type": response["type"],
            "content": [processed_result]
        }
    else:
        return response

# ------------deprecated
class Arg_add_memo(BaseModel):
    content: str

class Res_add_memo(BaseModel):
    memo_id: str
    tags: list[str]

@app.post("/add_memo/", response_model=Res_add_memo, status_code=status.HTTP_201_CREATED)
async def add_memo(body: Arg_add_memo):
    tags=qe.query_extractor(body.content)

    tag_name_list: list[str]=[tag_name for tag_name, tag_id in tags]
    tag_id_list: list[str]=[tag_id for tag_name, tag_id in tags]

    # TODO: separate db logics
    from langchain_openai import OpenAIEmbeddings
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small")
    memo_id: str=database.collections.memo_store.add_documents([
        Document(page_content=body.content, tags=tag_id_list, vector=embeddings.embed_query(body.content))
    ])[0]
    logging.info(f"[/add_memo] content: {body.content} / tags: {tags}")
    
    return {
        "memo_id": str(memo_id),
        "tags": tag_name_list,
    }

# ------------
@app.post("/_drop_all_db_and_reload/")
def _drop_all_db_and_reload():
    from drop_all_collections import drop_db
    drop_db()
    import os
    import signal
    os.kill(os.getpid(), signal.SIGINT)

@app.post("/_reload/")
def _reload():
    from drop_all_collections import drop_db
    drop_db()
    import os
    import signal
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == '__main__':
    uvicorn.run(app)

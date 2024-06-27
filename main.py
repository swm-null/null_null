# from database import connection
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pymilvus import MilvusClient
from ai.for_search import query_analyzer as qa
from ai.for_search import regex_generator as rg
from ai.for_search import tag_finder as tf
from ai.for_search import similarity_search as ss
from ai.for_save import query_extractor as qe
from logger import logger as lg
import traceback
import uvicorn, uvicorn.logging
import logging, logging.handlers
import datetime
import database.collections
from langchain_core.documents.base import Document

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    now = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
    handler = logging.handlers.TimedRotatingFileHandler(f'./logs/access/access_log_{now}.log', when='midnight', interval=1, backupCount=1)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    
@app.get("/")
async def default():
    return "yes. it works."

class Res_get_user_query(BaseModel):
    type: int
    content: list[str]

@app.get("/user_query/", response_model=Res_get_user_query)
async def get_user_query(query: str):
    query_type=qa.query_analyzer(query)

    return_content: Optional[list[str]]=None

    try:
        if query_type == qa.Query_Type.regex.name:
            query_type=2
            return_content=rg.get_regex(query)

        elif query_type == qa.Query_Type.find_tag.name:
            query_type=3
            return_content=tf.find_tag_name(query)

        if query_type == qa.Query_Type.similarity_search.name or return_content==None:
            query_type=1
            return_content=ss.search_similar_memos(query)
    except:
        lg.logger.error(traceback.format_exc())
        query_type=0

    lg.logger.info("user query: %s / query type: %s / %s", query, query_type, str(return_content))

    return {
        "type": query_type,
        "content": return_content
    }

class Arg_add_memo(BaseModel):
    content: str

class Res_add_memo(BaseModel):
    memo_id: str
    tags: list[str]

@app.post("/add_memo/", response_model=Res_add_memo)
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
    lg.logger.info(f"[ADD_MEMO] content: {body.content} / tags: {tags}")
    
    return {
        "memo_id": str(memo_id),
        "tags": tag_name_list,
    }

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


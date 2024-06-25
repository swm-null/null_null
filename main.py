# from database import connection
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pymilvus import MilvusClient
from ai import query_analyzer as qa
from ai import regex_generator as rg
from ai import tag_finder as tf
from ai import similarity_search as ss
from logger import logger as lg
import traceback
import uvicorn, uvicorn.logging
import logging, logging.handlers
import datetime

app = FastAPI()

# def get_db() -> MilvusClient:
#     return connection.db_client

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

@app.get("/user_query/")
async def get_user_query(query: str):
    query_type=qa.query_analyzer(query)

    return_content:Optional[str | list[str]]=None
    try:
        ## todo case 문정리
        if query_type == qa.Query_Type.regex.name:
            ## todo type을 String
            query_type=2
            return_content=rg.get_regex(query)
        elif query_type == qa.Query_Type.find_tag.name:
            query_type=3
            return_content=tf.find_tag_name(query)
            if len(return_content) == 0:
                query_type=qa.Query_Type.similarity_search.name

        if query_type == qa.Query_Type.similarity_search.name:
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

if __name__ == '__main__':
    uvicorn.run(app)

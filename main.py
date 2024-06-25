# from database import connection
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pymilvus import MilvusClient
from ai import query_analyzer as qa
from ai import regex_generator as rg
from ai import tag_finder as tf
from ai import similarity_search as ss
import traceback
import uvicorn
from uvicorn.config import LOGGING_CONFIG

app = FastAPI()

# def get_db() -> MilvusClient:
#     return connection.db_client

@app.get("/")
async def default():
    return "yes. it works."

@app.get("/user_query/")
async def get_user_query(query: str):
    query=query
    query_type=qa.query_analyzer(query)

    return_content:Optional[str | list[str]]=None

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
        print(traceback.format_exc())
        query_type=0

    print("user query:", query)
    print("query_type", query_type)
    print("return_content:", return_content)

    return {
        "type": query_type,
        "content": return_content
    }

@app.get("/user_query_with_processed_output/")
async def get_user_query_with_processed_output(query: str):
    query=query
    query_type=qa.query_analyzer(query)

    return_content:Optional[str | list[str]]=None
    try:
        if query_type == qa.Query_Type.regex.name:
            query_type=2
            return_content=rg.get_regex(query)

        elif query_type == qa.Query_Type.find_tag.name:
            query_type=3
            return_content=tf.find_tag_name(query)
            if len(return_content) == 0:
                query_type=qa.Query_Type.similarity_search.name

        if query_type == qa.Query_Type.similarity_search.name:
            query_type=1
            return_content=ss.search_similar_memos_with_processed_output(query)
    except:
        print(traceback.format_exc())
        query_type=0

    print("user query:", query)
    print("query_type", query_type)
    print("return_content:", return_content)

    return {
        "type": query_type,
        "content": return_content
    }

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app)

if __name__ == '__main__':
    run()

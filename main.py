from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from database import connection
from pymilvus import MilvusClient
from ai import query_analyzer as qa
from ai import regex_generator as rg
from ai import tag_finder as tf
# from ai import similarity_search as ss

app = FastAPI()

# def get_db() -> MilvusClient:
#     return connection.db_client

@app.get("/")
async def default():
    return "yes. it works."

class User_Query(BaseModel):
    content: str

@app.get("/user_query/")
async def get_user_query(user_query: User_Query):
    query=User_Query.content
    query_type=qa.query_analyzer(query)

    return_content:Optional[str | list[str]]=None
    if query_type == qa.Query_Type.regex:
        return_content=rg.get_regex(query)
    elif query_type == qa.Query_Type.find_tag:
        return_content=tf.find_tag_id(query)
    # elif query_type == qa.Query_Type.similarity_search:
    #     return_content=ss.search_similar_memos(query)

    return {
        "type": query_type,
        "content": return_content
    }



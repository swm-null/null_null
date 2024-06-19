from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from database import connection
from pymilvus import MilvusClient
from ai import query_analyzer as qa

app = FastAPI()

def get_db() -> MilvusClient:
    return connection.db_client

@app.get("/")
async def default():
    return "yes. it works."

class User_Query:
    content: str

@app.get("/user_query")
async def get_user_query(user_query: User_Query):
    analyzed_result=qa.query_analyzer(user_query.content)
    



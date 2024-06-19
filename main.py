from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from database import connection
from pymilvus import MilvusClient

app = FastAPI()

def get_db() -> MilvusClient:
    return connection.db_client

@app.get("/")
async def default():
    return "yes. it works."


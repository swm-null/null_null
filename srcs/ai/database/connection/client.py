import logging
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi


load_dotenv()

MONGO_SRV: str=str(os.getenv("MONGO_SRV"))
if MONGO_SRV == "None":
    raise Exception("[vectorstores.connection] Invalid MONGO_SRV")

def _get_db_name() -> str:
    FLOW: str=(str(os.getenv("FLOW")))
    DB_NAME_PROD: str=str(os.getenv("DB_NAME_PROD"))
    DB_NAME_STAGE: str=str(os.getenv("DB_NAME_STAGE"))
    
    return DB_NAME_STAGE if FLOW=="STAGE" else DB_NAME_PROD

DB_NAME=_get_db_name()
if DB_NAME == "None":
    raise Exception("[vectorstores.connection] Invalid DB_NAME")

ca=certifi.where()
client=MongoClient(MONGO_SRV, tlsCAFile=ca)

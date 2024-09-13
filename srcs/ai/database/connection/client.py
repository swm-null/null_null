from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi


load_dotenv()

FLOW: str=(str(os.getenv("FLOW")))
DB_NAME_PROD: str=str(os.getenv("DB_NAME"))
DB_NAME_STAGE: str=str(os.getenv("DB_NAME"))
MONGO_SRV: str=str(os.getenv("MONGO_SRV"))

DB_NAME=DB_NAME_STAGE if FLOW=="stage" else DB_NAME_PROD

if DB_NAME == "None":
    raise Exception("[vectorstores.connection] Invalid DB_NAME")
if MONGO_SRV == "None":
    raise Exception("[vectorstores.connection] Invalid MONGO_SRV")

ca=certifi.where()
client=MongoClient(MONGO_SRV, tlsCAFile=ca)

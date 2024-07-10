from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi

load_dotenv()
DB_NAME=os.getenv("DB_NAME")

ca=certifi.where()
MONGO_SRV=os.getenv("MONGO_SRV")
client=MongoClient(MONGO_SRV, tlsCAFile=ca)

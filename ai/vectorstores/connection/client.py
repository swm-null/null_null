from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi

load_dotenv()
DB_NAME: str=str(os.getenv("DB_NAME"))
MONGO_SRV: str=str(os.getenv("MONGO_SRV"))

if DB_NAME == "None":
    raise Exception("[vectorstores.connection] Invalid DB_NAME")
if MONGO_SRV == "None":
    raise Exception("[vectorstores.connection] Invalid MONGO_SRV")

ca=certifi.where()
client=MongoClient(MONGO_SRV, tlsCAFile=ca)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

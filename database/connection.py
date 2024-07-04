from dotenv import load_dotenv
import os
from pymilvus import MilvusClient

load_dotenv()

MILVUS_URI=os.getenv("MILVUS_URI")
if MILVUS_URI == None:
    raise Exception("Invalid MILVUS_URI")

# DB_NAME=os.getenv("DB_NAME")
# if DB_NAME == None:
#     raise Exception("Invalid DB_NAME")

# client=MilvusClient(
#     uri=MILVUS_URI,
#     db_name=DB_NAME,
# )

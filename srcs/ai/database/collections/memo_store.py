from langchain_mongodb import MongoDBAtlasVectorSearch
from ai.database.connection.client import client, DB_NAME
from ai.utils import embedder


MEMO_COLLECTION_NAME="memos"
MEMO_INDEX_NAME="vector_index_memos"
MEMO_ID_NAME="_id"
MEMO_UID_NAME="uId"
MEMO_CONTENT_NAME="content"
MEMO_UTIME_NAME="uTime"

memo_collection=client[DB_NAME][MEMO_COLLECTION_NAME]
memo_store=MongoDBAtlasVectorSearch(
    collection=memo_collection,
    embedding=embedder,
    index_name=MEMO_INDEX_NAME,
    text_key=MEMO_CONTENT_NAME,
)

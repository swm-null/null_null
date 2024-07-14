from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from ai.vectorstores.connection.client import client, DB_NAME

MEMO_COLLECTION_NAME="memos"
MEMO_CONTENT_NAME="content"
MEMO_INDEX_NAME="vector_index_memos"

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

memo_collection=client[DB_NAME][MEMO_COLLECTION_NAME]
memo_store=MongoDBAtlasVectorSearch(
    collection=memo_collection,
    embedding=embeddings,
    index_name=MEMO_INDEX_NAME,
    text_key=MEMO_CONTENT_NAME,
)

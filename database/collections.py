from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
import database.connection as connection

MEMO_COLLECTION_NAME="memos"
TAG_COLLECTION_NAME="tags"

MEMO_CONTENT_NAME="content"
TAG_CONTENT_NAME="name"

MEMO_INDEX_NAME="vector_index_memos"
TAG_INDEX_NAME="vector_index_tags"

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

if connection.DB_NAME == None:
    raise Exception("Invalid DB_NAME")

memo_collection=connection.client[connection.DB_NAME][MEMO_COLLECTION_NAME]
memo_store=MongoDBAtlasVectorSearch(
    collection=memo_collection,
    embedding=embeddings,
    index_name=MEMO_INDEX_NAME,
    text_key=MEMO_CONTENT_NAME,
)

tag_collection=connection.client[connection.DB_NAME][TAG_COLLECTION_NAME]
tag_store=MongoDBAtlasVectorSearch(
    collection=tag_collection,
    embedding=embeddings,
    index_name=TAG_INDEX_NAME,
    text_key=TAG_CONTENT_NAME,
)

from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from ai.database.connection.client import client, DB_NAME
from ai.utils.embedder import embedder


TAG_COLLECTION_NAME="tags"
TAG_CONTENT_NAME="name"
TAG_ID_NAME="_id"
TAG_INDEX_NAME="vector_index_tags"
TAG_UID_NAME="uId"
TAG_ROOT_NAME="@"

tag_collection=client[DB_NAME][TAG_COLLECTION_NAME]
tag_store=MongoDBAtlasVectorSearch(
    collection=tag_collection,
    embedding=embedder,
    index_name=TAG_INDEX_NAME,
    text_key=TAG_CONTENT_NAME,
)

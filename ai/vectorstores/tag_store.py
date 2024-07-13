from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from connection.client import client, DB_NAME

TAG_COLLECTION_NAME="tags"
TAG_CONTENT_NAME="name"
TAG_INDEX_NAME="vector_index_tags"

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

tag_collection=client[DB_NAME][TAG_COLLECTION_NAME]
tag_store=MongoDBAtlasVectorSearch(
    collection=tag_collection,
    embedding=embeddings,
    index_name=TAG_INDEX_NAME,
    text_key=TAG_CONTENT_NAME,
)

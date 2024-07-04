from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
import database.connection as connection

MEMO_NAME="memos"
TAG_NAME="tags"

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

memo_store=Milvus(
    embedding_function=embeddings,
    collection_name=MEMO_NAME,
    connection_args={
        "uri": connection.MILVUS_URI,
        # "db_name": connection.DB_NAME,
    },
    auto_id=True,
)

tag_store=Milvus(
    embedding_function=embeddings,
    collection_name=TAG_NAME,
    connection_args={
        "uri": connection.MILVUS_URI,
        # "db_name": connection.DB_NAME,
    },
    auto_id=True,
)

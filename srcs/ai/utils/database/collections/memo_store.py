from ai.utils.database.connection import client, DB_NAME


MEMO_COLLECTION_NAME="memos"
MEMO_INDEX_NAME="vector_index_memos"
MEMO_METADATA_INDEX_NAME="vector_index_memos_metadata"

MEMO_ID_NAME="_id"
MEMO_UID_NAME="uId"
MEMO_CONTENT_NAME="content"
MEMO_METADATA_NAME="metadata"
MEMO_UTIME_NAME="uTime"

MEMO_CONTENT_EMBEDDING_PATH="embedding"
MEMO_METADATA_EMBEDDING_PATH="embedding_metadata"

memo_collection=client[DB_NAME][MEMO_COLLECTION_NAME]

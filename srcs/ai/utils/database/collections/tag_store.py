from ai.utils.database.connection import client, DB_NAME


TAG_COLLECTION_NAME="tags"
TAG_CONTENT_NAME="name"
TAG_ID_NAME="_id"
TAG_INDEX_NAME="vector_index_tags"
TAG_UID_NAME="uId"
TAG_ROOT_NAME="@"

tag_collection=client[DB_NAME][TAG_COLLECTION_NAME]

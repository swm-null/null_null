from ai.database.connection.client import client, DB_NAME


COLLECTION_NAME="tag_edges"
UID_FIELD_NAME="uId"
EDGES_FIELD_NAME="edges"

tag_edges_collection=client[DB_NAME][COLLECTION_NAME]

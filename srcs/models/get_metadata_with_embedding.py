from pydantic import BaseModel


class Body_get_metadata_with_embedding(BaseModel):
    content: str
    images: list[str]

class Res_get_metadata_with_embedding(BaseModel):
    metadata: str
    embedding_metadata: list[float]

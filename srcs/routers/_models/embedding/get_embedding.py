from pydantic import BaseModel


class Body_get_embedding(BaseModel):
    content: str

class Res_get_embedding(BaseModel):
    embedding: list[float]

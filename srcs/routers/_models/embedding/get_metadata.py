from pydantic import BaseModel


class Body_get_metadata(BaseModel):
    content: str

class Res_get_metadata(BaseModel):
    metadata: str

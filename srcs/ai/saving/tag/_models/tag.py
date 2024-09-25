from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str = Field(description="name of tag")
    id: str = Field(description="id of tag")

from pydantic import BaseModel, Field
from routers._models.parser._models import Kakao_parser_type


class Body_post_kakao_parser(BaseModel):
    user_id: str
    type: Kakao_parser_type
    content: str=Field(description="url of content")

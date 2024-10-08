from pydantic import BaseModel
from enum import Enum

class kakao_parser_type(Enum):
    CSV="csv"
    TXT="txt"

class Body_post_kakao_parser(BaseModel):
    user_id: str
    type: kakao_parser_type
    content: str

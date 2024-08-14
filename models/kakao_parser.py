from pydantic import BaseModel
from enum import Enum
from models.add_memo import Res_add_memo

class kakao_parser_type(Enum):
    CSV="csv"
    TXT="txt"

class Arg_kakao_parser(BaseModel):
    type: kakao_parser_type
    content: str

class Res_kakao_parser(BaseModel):
    kakao: list[Res_add_memo]
